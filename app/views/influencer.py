from flask import Blueprint, render_template

influencer = Blueprint("influencer", __name__)


@influencer.route("/inf")
def dashboard():
    return render_template("influencer/dashboard.html")
