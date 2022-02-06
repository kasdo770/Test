import bcrypt
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config["SECRET_KEY"] = "43adf1abf54ce503ccdfdfdd"
db = SQLAlchemy(app)
bcrypts = Bcrypt(app)

login_man = LoginManager(app)
login_man.login_view = "login_page"
from market import routes
