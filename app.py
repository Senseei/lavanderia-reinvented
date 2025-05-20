from cs50 import SQL
from flask import Flask, request, redirect, render_template, session, jsonify
from flask_session import Session
from infrastructure.flask.routes.index_router import IndexRouter

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")
locations = db.execute("SELECT * FROM units")

app.register_blueprint(IndexRouter().blueprint)

# TODO
@app.route("/addpayment", methods=["GET", "POST"])
def addpayment():
    if not session["user_id"] or not session.get("user_id"):
        return redirect("/")

    if request.method == "POST":
        if not request.form.get("titular") or not request.form.get("cardnumber") or not request.form.get("validade") or not request.form.get("cvv"):
            return render_template("alert.html", message="Could not add your card.. Missing data!", path="/addpayment")

        cardnumber = int(request.form.get("cardnumber").replace(" ", ""))
        flag = request.form.get("flag")
        method = request.form.get("method")
        validade = request.form.get("validade")
        cv = request.form.get("cvv")

        rows = db.execute("SELECT * FROM cards WHERE cardnumber = ? AND method = ? AND user_id = ?", cardnumber, method, session["user_id"])
        if len(rows) > 0:
            return render_template("alert.html", message="You have already added this card!", path="/addpayment")

        db.execute("INSERT INTO cards (user_id, flag, cardnumber, method, validade, cv) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], flag, cardnumber, method, validade, cv)

        return render_template("alert.html", message="Success!", path="/mycards")

    return render_template("addpayment.html")


# TODO
@app.route("/cart", methods=["GET", "POST"])
def cart():
    if not session.get("user_id"):
        return redirect("/login")

    if "cart" not in session:
        session["cart"] = []
        session["total_in_cart"] = 0.0

    if request.method == "POST":
        tmpDict = {}
        tmpDict2 = {}
        product = {}

        machines = db.execute("SELECT * FROM machines WHERE id = ?", request.form.get("machine_id"))
        prices = db.execute("SELECT * FROM cycles WHERE id = ?", request.form.get("price_id"))

        tmpDict["machine_id"] = machines[0]["id"]
        tmpDict["type"] = machines[0]["type"]
        tmpDict["unit_id"] = machines[0]["unit_id"]

        tmpDict2["cycle_id"] = prices[0]["id"]
        tmpDict2["fprice"] = br(prices[0]["price"])
        tmpDict2["price"] = prices[0]["price"]
        tmpDict2["time"] = prices[0]["time"]

        product.update(tmpDict)
        product.update(tmpDict2)

        if product in session["cart"]:
            return render_template("alert.html", message="This product is already in your cart!", path="/local")

        session["cart"].append(product)
        session["total_in_cart"] += prices[0]["price"]

        return render_template("alert.html", message="Added to your cart :)", path="/local")

    return render_template("cart.html", total=br(session["total_in_cart"]))


# TODO
@app.route("/details", methods=["GET", "POST"])
def details():
    if not session.get("machine") and not request.form.get("id"):
        return render_template("alert.html", message="Please, select an unit and then a machine!", path="/")

    if request.form.get("id"):
        session["machine"] = request.form.get("id")

    islocked = db.execute("SELECT * FROM machines WHERE id = ?", session["machine"])

    if int(islocked[0]["locked"]) == 1:
        return render_template("alert.html", message="Ops, looks like this machine is already in use!", path="/local")

    prices = []

    machine_id = request.form.get("id")
    machine = db.execute("SELECT * FROM machines WHERE id = ?", machine_id)

    cycles = db.execute("SELECT * FROM cycles ORDER BY time")

    for cycle in cycles:
        tmpDict = {}
        tmpDict.update(cycle)

        tmpDict["price"] = br(float(tmpDict["price"]))

        prices.append(tmpDict)

    return render_template("details.html", machine=machine[0], prices=prices)
    

# TODO
@app.route("/local", methods=["GET", "POST"])
def local():
    if not session.get("unit") and not request.form.get("id"):
        return render_template("alert.html", message="Select an unit!", path="/")

    if request.form.get("id"):
        session["unit"] = request.form.get("id")

    washers = db.execute("SELECT * FROM machines WHERE unit_id = ? AND type = 'Lavadora'", session["unit"])
    dryers = db.execute("SELECT * FROM machines WHERE unit_id = ? AND type = 'Secadora'", session["unit"])

    return render_template("local.html", washers=washers, dryers=dryers)

# TODO
@app.route("/payment", methods=["GET", "POST"])
def payment():
    if not session.get("user_id"):
        return redirect("/login")

    if "cart" not in session or not session["cart"]:
        return redirect("/cart")

    if request.method == "POST":

        busy_machines = 0
        for i in range(len(session["cart"])):
            machine = db.execute("SELECT * FROM machines WHERE id = ?", session["cart"][i]["machine_id"])
            if machine[0]["locked"] == 1:
                del session["cart"][i]
                busy_machines += 1

        if busy_machines > 0:
            return render_template("alert.html", message="Error finishing the payment, one or more machines are busy! So I removed them from your cart.", path="/cart")


        if int(request.form.get("payment_method")) == 0:
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", session["total_in_cart"], session["user_id"])
            session["cash"] = br(db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"] - session["total_in_cart"])

        for machine in session["cart"]:
            db.execute("UPDATE machines SET locked = 1 WHERE id = ?", machine["machine_id"])
            db.execute("INSERT INTO history (user_id, unit_id, machine_id, cycle_id) VALUES (?, ?, ?, ?)", session["user_id"], machine["unit_id"], machine["machine_id"], machine["cycle_id"])

        del session["cart"]

        return render_template("alert.html", message="Success!", path="/local")

    if "discounts" not in session or not session["discounts"]:
        session["discounts"] = 0.0

    payment_info = {
        "products": br(session["total_in_cart"]),
        "total": br(session["total_in_cart"] - session["discounts"]),
        "discounts": br(session["discounts"]),
        "cards": []    
    }

    cards = db.execute("SELECT * FROM cards WHERE user_id = ?", session["user_id"])

    for card in cards:
        tmpDict = {}
        tmpDict.update(card)

        tmpDict["final"] = int(card["cardnumber"]) % 10000

        payment_info["cards"].append(tmpDict)

    return render_template("payment.html", payment_info=payment_info)

# TODO
@app.route("/mycards")
def mycards():
    if not session["user_id"]:
        return redirect("/")

    rows = db.execute("SELECT * FROM cards WHERE user_id = ?", session["user_id"])
    cards = []

    for card in rows:
        tmpDict = {}
        tmpDict.update(card)
        final = "**** **** **** "
        for i in range(4):
            number = str(card["cardnumber"])
            final = final + number[len(number) - 4 + i]
        tmpDict["final"] = final

        cards.append(tmpDict)

    return render_template("payments.html", cards=cards)

# TODO
@app.route("/rmvfromcart", methods=["GET", "POST"])
def rmv():
    if not request.form.get("cycle_id") and not request.form.get("machine_id"):
        return redirect("/cart")

    for i in range(len(session["cart"])):
        if int(session["cart"][i]["cycle_id"]) == int(request.form.get("cycle_id")) and int(session["cart"][i]["machine_id"]) == int(request.form.get("machine_id")):
            session["total_in_cart"] -= session["cart"][i]["price"]
            del(session["cart"][i])

            return redirect("/cart")

    return redirect("/cart")


# TODO
@app.route("/rmvcard", methods=["GET", "POST"])
def rmvcard():
    if not session["user_id"]:
        return redirect("/")

    if request.method == "POST":
        card_id = request.form.get("card_id")

        db.execute("DELETE FROM cards WHERE id = ?", card_id)

    return redirect("/mycards")


def br(value):
    return f"R${value:,.2f}"
