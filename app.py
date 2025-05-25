from cs50 import SQL
from flask import Flask, request, redirect, render_template, session, jsonify
from flask_session import Session
from infrastructure.flask.routes.index_router import IndexRouter

app = Flask(__name__,
           static_folder='infrastructure/flask/resources/static',
           template_folder='infrastructure/flask/resources/templates')

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

    return render_template("add_payment.html")

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
