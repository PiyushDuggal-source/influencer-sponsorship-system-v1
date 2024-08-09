from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.campaign import Campaign
from app.extensions import db
from app.forms import CampaignForm
from app.models.ad_request import AdRequest
from app.forms import AdRequestForm

# from datetime import datetime

sponsor = Blueprint("sponsor", __name__)


@sponsor.route("/campaigns")
@login_required
def campaigns():
    campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()
    return render_template("sponsor/campaigns.html", campaigns=campaigns)


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
    return render_template("sponsor/create_campaign.html", form=form)


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
    return render_template("sponsor/update_campaign.html", form=form, campaign=campaign)


@sponsor.route("/campaign/<int:id>/delete", methods=["POST"])
@login_required
def delete_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    if campaign.sponsor_id != current_user.id:
        flash("You do not have permission to delete this campaign.", "danger")
        return redirect(url_for("sponsor.campaigns"))

    db.session.delete(campaign)
    db.session.commit()
    flash("Campaign deleted successfully!", "success")
    return redirect(url_for("sponsor.campaigns"))


@sponsor.route("/campaigns/<int:campaign_id>/ad-requests")
@login_required
def ad_requests(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        flash("You do not have permission to view this campaign.", "danger")
        return redirect(url_for("sponsor.campaigns"))

    ad_requests = campaign.ad_requests
    return render_template(
        "sponsor/ad_requests.html", campaign=campaign, ad_requests=ad_requests
    )


@sponsor.route(
    "/campaigns/<int:campaign_id>/ad-requests/create", methods=["GET", "POST"]
)
@login_required
def create_ad_request(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.sponsor_id != current_user.id:
        flash(
            "You do not have permission to create ad requests for this campaign.",
            "danger",
        )
        return redirect(url_for("sponsor.campaigns"))

    form = AdRequestForm()
    if form.validate_on_submit():
        ad_request = AdRequest(
            campaign_id=campaign.id,
            influencer_id=form.influencer_id.data,
            requirements=form.requirements.data,
            payment_amount=form.payment_amount.data,
        )
        db.session.add(ad_request)
        db.session.commit()
        flash("Ad request created successfully!", "success")
        return redirect(url_for("sponsor.ad_requests", campaign_id=campaign.id))
    return render_template(
        "sponsor/create_ad_request.html", form=form, campaign=campaign
    )


@sponsor.route("/ad-requests/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_ad_request(id):
    ad_request = AdRequest.query.get_or_404(id)
    campaign = ad_request.campaign
    if campaign.sponsor_id != current_user.id:
        flash("You do not have permission to edit this ad request.", "danger")
        return redirect(url_for("sponsor.ad_requests", campaign_id=campaign.id))

    form = AdRequestForm(obj=ad_request)
    if form.validate_on_submit():
        form.populate_obj(ad_request)
        db.session.commit()
        flash("Ad request updated successfully!", "success")
        return redirect(url_for("sponsor.ad_requests", campaign_id=campaign.id))
    return render_template(
        "sponsor/update_ad_request.html", form=form, ad_request=ad_request
    )


@sponsor.route("/ad-requests/<int:id>/delete", methods=["POST"])
@login_required
def delete_ad_request(id):
    ad_request = AdRequest.query.get_or_404(id)
    campaign = ad_request.campaign
    if campaign.sponsor_id != current_user.id:
        flash("You do not have permission to delete this ad request.", "danger")
        return redirect(url_for("sponsor.ad_requests", campaign_id=campaign.id))

    db.session.delete(ad_request)
    db.session.commit()
    flash("Ad request deleted successfully!", "success")
    return redirect(url_for("sponsor.ad_requests", campaign_id=campaign.id))
