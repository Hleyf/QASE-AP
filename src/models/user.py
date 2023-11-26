from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)
    full_name = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False, unique=False)
    #  created_by has a one to many relationship with user
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.relationship('User', backref=db.backref('created_users', lazy='dynamic'), foreign_keys=[created_by_id])
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    updated_by = db.relationship('User', backref=db.backref('updated_users', lazy='dynamic'), foreign_keys=[updated_by_id])
    created_at = db.Column(db.DateTime, nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, nullable=True, unique=False)

    
    
    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        try:
            self.password = generate_password_hash(password)
        except Exception as e:
            raise e
        
    def check_password(self, password):
        try:
            return check_password_hash(self.password, password)
        except Exception as e:
            raise e

