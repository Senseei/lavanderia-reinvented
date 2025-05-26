from flask import Flask, request, redirect, render_template, session, jsonify
from flask_session import Session
from infrastructure.flask.routes.index_router import IndexRouter

app = Flask(__name__,
           static_folder='infrastructure/flask/resources/static',
           template_folder='infrastructure/flask/resources/templates')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(IndexRouter().blueprint)
