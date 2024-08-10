from flask import Blueprint, flash, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.models.user import User
from app.models.ad_request import AdRequest
from app.extensions import db
from app.forms import CampaignForm, InfluencerSearchForm, AdRequestForm
from flask_wtf.csrf import generate_csrf
from sqlalchemy import func

sponsor = Blueprint("sponsor", __name__)


@sponsor.route("/campaigns")
@login_required
def campaigns():
    if current_user.role != "sponsor":
        flash("Access denied. You must be a sponsor to view campaigns.", "danger")
        return redirect(url_for("main.home"))
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    return render_template(
        "sponsor/campaigns.html", campaigns=campaigns, user=current_user
    )


@sponsor.route("/campaign/create", methods=["GET", "POST"])
@login_required
def create_campaign():
    form = CampaignForm()
    print(form.data)
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            budget=form.budget.data,
            niche=form.niche.data,
            sponsor_id=current_user.id,
            visibility=form.visibility.data,
        )
        db.session.add(campaign)
        db.session.commit()
        flash("Campaign created successfully!", "success")
        return redirect(url_for("sponsor.campaigns"))
    return render_template("sponsor/create_campaign.html", form=form, user=current_user)


@sponsor.route("/campaign/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    if campaign.sponsor_id != current_user.id:
        flash("You do not have permission to edit this campaign.", "danger")
        return redirect(url_for("sponsor.campaigns"))

    form = CampaignForm(obj=campaign)
    if form.validate_on_submit():
        form.populate_obj(campaign)
        db.session.commit()
        flash("Campaign updated successfully!", "success")
        return redirect(url_for("sponsor.campaigns"))
    return render_template(
        "sponsor/update_campaign.html", form=form, campaign=campaign, user=current_user
    )


@sponsor.route("/campaign/<int:id>/delete", methods=["POST"])
@login_required
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    if campaign.sponsor_id != current_user.id:
        flash("You are not allowed to delete this.", "danger")
        return redirect(url_for("sponsor.campaigns"))

    db.session.delete(campaign)
    db.session.commit()
    flash("Campaign deleted successfully!", "success")
    return redirect(url_for("sponsor.campaigns"))


@sponsor.route("/search_influencers", methods=["GET", "POST"])
@login_required
def search_influencers():
    form = InfluencerSearchForm()

    influencers = []

    if form.validate_on_submit():
        niche = form.niche.data

        influencers = User.query.filter(
            User.role == "influencer", User.niche == niche
        ).all()

    return render_template(
        "sponsor/search_influencers.html",
        form=form,
        influencers=influencers,
        user=current_user,
    )


@sponsor.route(
    "/campaign/<int:campaign_id>/send_ad_request/<int:influencer_id>",
    methods=["GET", "POST"],
)
@login_required
def send_ad_request(campaign_id, influencer_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    influencer = User.query.get_or_404(influencer_id)

    if campaign.sponsor_id != current_user.id:
        flash(
            "You do not have permission to send ad requests for this campaign.",
            "danger",
        )
        return redirect(url_for("sponsor.campaigns"))

    form = AdRequestForm()

    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
            status="Pending",
        )
        db.session.add(ad_request)
        db.session.commit()
        flash("Ad request sent successfully!", "success")
        return redirect(url_for("sponsor.campaigns"))

    return render_template(
        "sponsor/send_ad_request.html",
        form=form,
        campaign=campaign,
        influencer=influencer,
        user=current_user,
    )


@sponsor.route("/select_campaign/<int:influencer_id>", methods=["GET", "POST"])
@login_required
def select_campaign(influencer_id):
    influencer = User.query.get_or_404(influencer_id)
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()

    if request.method == "POST":
        campaign_id = request.form.get("campaign_id")
        if campaign_id:
            return redirect(
                url_for(
                    "sponsor.send_ad_request",
                    campaign_id=campaign_id,
                    influencer_id=influencer_id,
                )
            )
        else:
            flash("Please select a campaign", "warning")

    return render_template(
        "sponsor/select_campaign.html",
        influencer=influencer,
        campaigns=campaigns,
        user=current_user,
        csrf_token=generate_csrf(),
    )

@sponsor.route("/stats")
@login_required
def stats():
    # Get all campaigns for the current sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    
    # Get total number of campaigns
    total_campaigns = len(campaigns)
    
    # Get total budget across all campaigns
    total_budget = sum(campaign.budget for campaign in campaigns)
    
    # Get total number of ad requests
    total_ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == current_user.id).count()
    
    # Get ad requests by status
    ad_requests_by_status = db.session.query(
        AdRequest.status, 
        func.count(AdRequest.id)
    ).join(Campaign).filter(
        Campaign.sponsor_id == current_user.id
    ).group_by(AdRequest.status).all()
    
    # Get top 5 campaigns by number of ad requests
    top_campaigns = db.session.query(
        Campaign.name, 
        func.count(AdRequest.id).label('request_count')
    ).join(AdRequest).filter(
        Campaign.sponsor_id == current_user.id
    ).group_by(Campaign.id).order_by(
        func.count(AdRequest.id).desc()
    ).limit(5).all()
    
    return render_template(
        "sponsor/stats.html",
        user=current_user,
        total_campaigns=total_campaigns,
        total_budget=total_budget,
        total_ad_requests=total_ad_requests,
        ad_requests_by_status=dict(ad_requests_by_status),
        top_campaigns=top_campaigns
    )
