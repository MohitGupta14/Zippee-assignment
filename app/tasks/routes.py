from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Task, User
from ..extensions import db
from .utils import validate_task_data

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    completed = request.args.get('completed')

    query = Task.query
    if user.role != 'admin':
        query = query.filter_by(user_id=user_id)
    if completed is not None:
        completed_bool = completed.lower() in ['true', '1', 'yes']
        query = query.filter_by(completed=completed_bool)

    query = query.order_by(Task.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = [t.to_dict() for t in pagination.items]

    return jsonify({
        'tasks': tasks,
        'pagination': {
            'page': page,
            'pages': pagination.pages,
            'per_page': per_page,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })

@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    task = Task.query.get_or_404(task_id)
    if user.role != 'admin' and task.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    return jsonify({'task': task.to_dict()})

@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    errors = validate_task_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False),
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Task created', 'task': task.to_dict()}), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    task = Task.query.get_or_404(task_id)

    if user.role != 'admin' and task.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json() or {}
    errors = validate_task_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'message': 'Task updated', 'task': task.to_dict()})

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    task = Task.query.get_or_404(task_id)
    if user.role != 'admin' and task.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})
