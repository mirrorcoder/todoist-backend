import json

from flask import Blueprint
from flask import Response
from flask import abort
from flask import request
from flask_cors import cross_origin

from extensions import db
from models.task import Task
from utils import row2dict, calc_pages

tasks = Blueprint('tasks', __name__, url_prefix = '/api/tasks')

TASKS_PER_PAGE = 3
TOKEN_STATIC_AUTH = 'static-token'

@tasks.route('', methods=['GET'])
@cross_origin()
def get_tasks():
    page = int(request.args.get('page', 1))-1
    field = request.args.get('field', 'id')
    direction = request.args.get('type', 'asc')
    if field not in ['id', 'name', 'email', 'status']:
        abort(500)
    if direction not in ['asc', 'desc']:
        abort(500)
    if page < 0:
        abort(500)
    pages = calc_pages(Task, page, TASKS_PER_PAGE)
    if field == 'name':
        model_by_order = Task.name_user.asc() if direction == 'asc' else Task.name_user.desc()
    elif field == 'email':
        model_by_order = Task.email_user.asc() if direction == 'asc' else Task.email_user.desc()
    elif field == 'status':
        model_by_order = Task.is_done.asc() if direction == 'asc' else Task.is_done.desc()
    else:
        model_by_order = Task.id.asc() if direction == 'asc' else Task.id.desc()
    tasks = Task.query.order_by(model_by_order).limit(TASKS_PER_PAGE).offset(TASKS_PER_PAGE*page)
    return {
        'pages': pages,
        'tasks': [row2dict(task) for task in tasks]
    }

@tasks.route('/', methods=['POST'])
@cross_origin()
def add_task():
    name_user = request.json.get('name_user', None)
    email_user = request.json.get('email_user', None)
    desc_task = request.json.get('desc_task', None)
    task = Task(name_user=name_user, email_user=email_user, desc_task=desc_task, is_done=False, is_edit_admin=False)
    db.session.add(task)
    db.session.commit()
    resp = Response(status=200)
    return resp

@tasks.route('/auth', methods=['POST'])
@cross_origin()
def auth_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username == 'admin' and password == '123':
        return Response(json.dumps({
            'success': True,
            'user_id': 1,
            'token': TOKEN_STATIC_AUTH
        }), status=200)
    abort(403)

@tasks.route('/<int:task_id>', methods=['POST'])
@cross_origin()
def update_task(task_id):
    token = request.json.get('token', None)
    desc = request.json.get('desc_task', None)
    is_done = request.json.get('is_done', None)
    if token != TOKEN_STATIC_AUTH:
        abort(403)
    task = Task.query.get(task_id)
    if not task:
        abort(404)
    if desc and (task.desc_task != desc):
        task.desc_task = desc
        task.is_edit_admin = True
    if is_done is not None:
        task.is_done = is_done
    db.session.add(task)
    db.session.commit()
    return Response(status=200)
