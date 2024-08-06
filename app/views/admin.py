from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.user import User
from app.models.campaign import Campaign
from app.models.ad_request import AdRequest
from flask_login import current_user

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        return {"message": "Not authorized"}, 403
    # Fetch statistics
    total_users = User.query.count()
    active_users = User.query.filter(User.is_active != None).count()
    total_campaigns = Campaign.query.count()
    public_campaigns = Campaign.query.filter_by(visibility="public").count()
    private_campaigns = Campaign.query.filter_by(visibility="private").count()
    total_ad_requests = AdRequest.query.count()
    pending_ad_requests = AdRequest.query.filter_by(status="pending").count()
    accepted_ad_requests = AdRequest.query.filter_by(status="accepted").count()
    rejected_ad_requests = AdRequest.query.filter_by(status="rejected").count()

    # # You might want to add a 'flagged' field to User model for this
    # flagged_users = User.query.filter_by(flagged=True).count()

    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "total_campaigns": total_campaigns,
        "public_campaigns": public_campaigns,
        "private_campaigns": private_campaigns,
        "total_ad_requests": total_ad_requests,
        "pending_ad_requests": pending_ad_requests,
        "accepted_ad_requests": accepted_ad_requests,
        "rejected_ad_requests": rejected_ad_requests,
        # "flagged_users": flagged_users,
    }

    return render_template("admin/dashboard.html", stats=stats, user=current_user)
