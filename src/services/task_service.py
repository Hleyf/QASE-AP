from datetime import datetime
from models.task import Task
from models import db
from flask_login import current_user
from flask import request

class TaskService:
    
    @classmethod
    def get_tasks(cls):
        try:
            page = request.args.get('page', 1, type=int)
            sort = request.args.get('sort', 'id', type=str)
            order = request.args.get('order', 'asc', type=str)
            per_page = request.args.get('per_page', 5, type=str)
            per_page = int(per_page)
            return Task.query.order_by(getattr(Task, sort).asc() if order == 'asc' else getattr(Task, sort).desc()).paginate(page=page, per_page=per_page)
        except Exception as e:
            raise e

    @classmethod
    def get_task_by_id(cls, task_id):
        try:
            return Task.query.get(task_id)
        except Exception as e:
            raise e
    
    @classmethod
    def create_task(cls, task):
        try:
            task.created_at = datetime.now()
            task.created_by = current_user.user_name
            db.session.add(task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def update_task(cls, task):
        try:
            task_db = Task.query.get(task.id)
            task_db.title = task.title
            task_db.description = task.description
            task_db.updated_at = datetime.now()
            task_db.updated_by = current_user.user_name
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def delete_task(cls, task_id):
        try:
            task = Task.query.get(task_id)
            db.session.delete(task)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def update_task_status(cls, task_id, status):
        try:
            task = Task.query.get(task_id)
            task.status = status
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def get_task_by_status(cls, status):
        try:
            tasks = Task.query.filter_by(status=status).all()
            return tasks
        except Exception as e:
            raise e
    
    @classmethod
    def get_task_by_user(cls, user_id):
        try:
            tasks = Task.query.filter_by(user_id=user_id).all()
            return tasks
        except Exception as e:
            raise e
    
    @classmethod
    def get_task_by_user_and_status(cls, user_id, status):
        try:
            tasks = Task.query.filter_by(user_id=user_id, status=status).all()
            return tasks
        except Exception as e:
            raise e
    