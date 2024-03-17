from api.models.user import UserModel
from api.auth.forms import RegistrationForm, LoginForm
from flask import abort, render_template, request, session, redirect, url_for, Blueprint, flash
from api import db

auth = Blueprint("auth", __name__)

@auth.get("/auth/")
@auth.get("/auth/home")
def home():
    return render_template("home.html")


@auth.route("/auth/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        flash("You are already logged in", "info")
        return redirect(url_for("auth.home"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        existing_username = UserModel.query.filter(UserModel.username.like("%" + username + "%")).one_or_none()
        
        if existing_username:
            flash("This username is already exists. Try another one. ", "warning")
            return render_template("register.html", form=form)

        user = UserModel(username, password)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception:
            abort(400, "Database commit operation failed.")
        flash("You are now registered. Please login.", "success")
        return redirect(url_for("auth.login"))

    if form.errors:
        flash(form.errors, "danger")
    return render_template("register.html", form=form)  


@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        existing_user = UserModel.query.filter_by(username=username).one_or_none()
        if not (existing_user and existing_user.verify_password(password)):
            flash("Invalid username or password. Please try again.", "danger")
            return render_template("login.html", form=form)  
    
        session["username"] = username
        flash("You have successfully login", "success")
        return redirect(url_for("auth.home"))

    if form.errors:
        flash(form.errors, "danger")
    return render_template("login.html", form=form)  


@auth.route("/auth/logout")
def logout():
    if "username" in session:
        session.pop("username")
        flash("You have successfully logout", "success")
    return redirect(url_for("auth.home"))