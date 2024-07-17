from flask_restful import Resource, reqparse
from app.models.campaign import Campaign
from app.extensions import db


class CampaignListAPI(Resource):
    def get(self):
        campaigns = Campaign.query.all()
        print(campaigns)
        return {"campaigns": campaigns}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("description", type=str, required=True)
        args = parser.parse_args()

        campaign = Campaign(name=args["name"], description=args["description"])
        db.session.add(campaign)
        db.session.commit()

        return {"message": "Campaign created successfully"}, 201


class CampaignAPI(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        return {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
        }

    def put(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("description", type=str)
        args = parser.parse_args()

        if args["name"]:
            campaign.name = args["name"]
        if args["description"]:
            campaign.description = args["description"]

        db.session.commit()
        return {"message": "Campaign updated successfully"}

    def delete(self, campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        db.session.delete(campaign)
        db.session.commit()
        return {"message": "Campaign deleted successfully"}
