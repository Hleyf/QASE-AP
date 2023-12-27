from datetime import datetime

from extensions import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(128), nullable=False, default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True), foreign_keys=[user_id])
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    created_by = db.relationship('User', foreign_keys=[created_by_id])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'user': {'id': self.user.id, 'user_name': self.user.user_name} if self.user else None,
            'created_by': {'id': self.created_by.id, 'user_name': self.created_by.user_name} if self.created_by else None,
            'created_at': self.created_at,
            'updated_by': {'id': self.updated_by.id, 'user_name': self.updated_by.user_name} if self.updated_by else None,
            'updated_at': self.updated_at,
    }