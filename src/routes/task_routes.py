

from flask import Blueprint, jsonify, render_template
from services import TaskService


task_routes = Blueprint('task_routes', __name__)
service = TaskService()

@task_routes.route('/tasks')
def tasks():
    tasks = service.get_tasks()
    return render_template('pages/task_list.html', tasks=tasks)

@task_routes.route('/tasks/<id>/edit', methods=['PUT'])
def update_task(id):
    task = service.get_task_by_id(id)
    return render_template('pages/edit-modal.html', task=task)


@task_routes.route('/tasks/create', methods=['POST'])
def create_task():
    task = service.create_task()
    if task.id:
        return jsonify({'success': True})
    return jsonify({'success': False})

@task_routes.route('/tasks/<id>/edit', methods=['POST'])
def update_task(id):
    task = service.update_task(id)
    if task.id:
        return jsonify({'success': True})
    return jsonify({'success': False})

@task_routes.route('/tasks/<id>/delete', methods=['DELETE'])
def delete_task(id):
    service.delete_task(id)
    return jsonify({'success': True})

@task_routes.route('/tasks/<id>/status/<status>', methods=['POST'])
def update_task_status(id, status):
    service.update_task_status(id, status)
    return jsonify({'success': True})


