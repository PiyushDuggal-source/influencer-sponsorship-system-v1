from flask import Flask
from app.extensions import db, login_manager, csrf, api_ref
from app.api.campaigns import CampaignListAPI, CampaignAPI
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.views import auth, sponsor, influencer, admin

    app.register_blueprint(auth.auth)
    app.register_blueprint(sponsor.sponsor)
    # app.register_blueprint(influencer)
    # app.register_blueprint(admin.bp)

    # Register API resources
    api_ref.add_resource(CampaignListAPI, "/api/campaigns")
    api_ref.add_resource(CampaignAPI, "/api/campaigns/<int:campaign_id>")

    api_ref.init_app(app)
    return app
