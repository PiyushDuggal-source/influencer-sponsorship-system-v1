from app.extensions import db
from datetime import datetime

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float)
    visibility = db.Column(db.String(10))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    sponsor = db.relationship('User', backref='campaigns')
