from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.extensions import db

sponsor = Blueprint("sponsor", __name__)


@sponsor.route("/dashboard")
@login_required
def sponsor_dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    return render_template("sponsor/dashboard.html", campaigns=campaigns)


@sponsor.route("/create_campaign", methods=["GET", "POST"])
@login_required
def create_campaign():
    if request.method == "POST":
        # Create campaign logic here
        pass
    return render_template("sponsor/create_campaign.html")
