from app.extensions import db

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(20))

    campaign = db.relationship('Campaign', backref='ad_requests')
    influencer = db.relationship('User', backref='ad_requests')
