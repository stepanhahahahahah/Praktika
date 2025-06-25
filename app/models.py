from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password = db.Column(db.String(120), nullable=False) 
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    telegram_id = db.Column(db.String(60), nullable=True)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'

class Client(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False) 
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Membership {self.membership_type}>'

class Event(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    
    
    def __repr__(self):
        return f'<Workout {self.title}>'