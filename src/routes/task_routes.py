

from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from services import TaskService
from models import Task

task_routes = Blueprint('task_routes', __name__)
service = TaskService()

@task_routes.route('/tasks')
@login_required
def tasks():
    tasks = service.get_tasks()
    return render_template('pages/task_list.html', tasks=tasks)

@task_routes.route('/tasks/<id>/json', methods=['GET'])
@login_required
def get_task_as_json(id):
    task = service.get_task_by_id(int(id))
    return jsonify(task.to_dict())

@task_routes.route('/task/<id>/update', methods=['POST'])
@login_required
def update_task(id):
    task_id = service.update_task(id)
    if task_id:
        return redirect(url_for('task_routes.tasks'))



@task_routes.route('/task/create', methods=['POST'])
@login_required
def create_task():
    user_id = int(request.form.get('user')) if request.form.get('user') else None
    task = Task(
        title=request.form.get('title'),
        description=request.form.get('description'),
        status=request.form.get('status'),
        user_id=user_id
    )
    task_id = service.create_task(task)
    if task_id:
        return redirect(url_for('task_routes.tasks'))
    else:
        return render_template('pages/task_modal.html', error="Invalid credentials")

@task_routes.route('/tasks/<id>/delete', methods=['DELETE'])
@login_required
def delete_task(id):
    service.delete_task(id)
    return jsonify({'success': True})
