from flask import flash
from flask_login.utils import login_required
from flask_wtf import form
from market import app
from flask import render_template, redirect, url_for
from market.models import User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required


@app.route("/cleartable")
@app.route("/ct")
def clear_table():
    db.drop_all()
    db.create_all()
    flash("database is cleared with User Table !", category="info")
    return redirect(url_for("market_page"))


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market")
@login_required
def market_page():
    return render_template("market.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        db.create_all()
        user_to_create = User(
            username=register_form.username.data,
            email_address=register_form.email.data,
            password=register_form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        db.session.query(User).delete()
        flash(
            f"Account is created with name : {register_form.username.data}",
            category="success",
        )
        return redirect(url_for("market_page"))
    if register_form.errors != {}:
        for err_msg in register_form.errors.values():
            flash(
                f"The was an an Error with creating user :  {err_msg}", category="error"
            )

    return render_template("register.html", form=register_form)


@app.route("/login", methods=["POST", "GET"])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            if user.password_check(thepass=login_form.password.data):
                login_user(user)
                flash(
                    f"Logged in successfully as {login_form.username.data} !",
                    category="success",
                )
                return redirect(url_for("market_page"))
            else:
                flash("Password is incorrect")
        else:
            flash("There is no account with this username", category="error")
        return render_template("market.html")
    return render_template("login.html", form=login_form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("home_page"))
