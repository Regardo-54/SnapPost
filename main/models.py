from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from main import db,login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(20), unique=True, nullable=False)
    email =  db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable = False, default="https://i.ibb.co/1QywQ5D/profile-1.png")
    password =  db.Column(db.Unicode, nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True )

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=300):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,max_age=expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)
    

class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    image = db.Column(db.String(20),nullable = False, default=" ")
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
