from flask import Blueprint
from flask import abort
from flask import request

from extensions import db
from models.task import Task
from utils import row2dict, calc_pages

tasks = Blueprint('tasks', __name__, url_prefix = '/api/tasks')

TASKS_PER_PAGE = 3

@tasks.route('', methods=['GET'])
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
    model_by_order = None
    if field == 'name':
        model_by_order = Task.name_user.asc() if direction == 'asc' else Task.name_user.desc()
    elif field == 'email':
        model_by_order = Task.email_user.asc() if direction == 'asc' else Task.email_user.desc()
    elif field == 'status':
        model_by_order = Task.is_done.asc() if direction == 'asc' else Task.is_done.desc()
    if field != 'id':
        tasks = Task.query.order_by(model_by_order)
    else:
        tasks = Task.query
    tasks = tasks.limit(TASKS_PER_PAGE).offset(TASKS_PER_PAGE*page)
    return {
        'pages': pages,
        'tasks': [row2dict(task) for task in tasks]
    }

@tasks.route('', methods=['POST'])
def add_task():
    name_user = request.json.get('name_user', None)
    email_user = request.json.get('email_user', None)
    desc_task = request.json.get('desc_task', None)
    task = Task(name_user=name_user, email_user=email_user, desc_task=desc_task, is_done=False)
    db.session.add(task)
    db.session.commit()
    return {
        'task_id': task.id
    }

