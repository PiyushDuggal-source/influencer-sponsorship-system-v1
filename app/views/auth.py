from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from flask_wtf.csrf import generate_csrf

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # Login logic here
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))  # Redirect if user is already logged in

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        print(username, password, role)

        user = User.query.filter_by(username=username, role=role).first()
        print(user)

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html", csrf_token=generate_csrf())


@auth.route("/register", methods=["GET", "POST"])
def register():
    # Registration logic here
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        role = request.form.get("role")
        print(username, email, password, confirm_password, role)

        user_by_username = User.query.filter_by(username=username).first()

        if password != confirm_password:
            flash("Passwords do not match", "warning")
            return redirect(url_for("auth.register"))

        if user_by_username:
            flash("Username already exists", "warning")
            return redirect(url_for("auth.register"))

        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash("Email address already exists", "warning")
            return redirect(url_for("auth.register"))

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", csrf_token=generate_csrf())


@auth.route("/debug-users")
def debug_users():
    users = User.query.all()
    print("users", users)

    print(users)
    return "Check your console for user data."


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))
