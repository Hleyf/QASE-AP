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
    created_by = db.Column(db.String, nullable=False, unique=False)   
    created_at = db.Column(db.DateTime, nullable=False, unique=False)
    updated_by = db.Column(db.Integer, nullable=True, unique=False) 
    updated_at = db.Column(db.DateTime, nullable=True, unique=False)

    
    
    def __repr__(self):
        return '<User %r>' % self.user_name

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

