# -*- encoding: utf-8

from flask import jsonify, request, render_template, redirect, url_for

from . import app
from .tasks import find_untagged_posts_task, States


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    return redirect(url_for('index'))


@app.route('/trigger_task', methods=['POST'])
def trigger_task():
    hostname = request.args['hostname']
    task = find_untagged_posts_task.apply_async((hostname, ))
    return jsonify({}), 202, {
        'Location': url_for('task_status', task_id=task.id),
    }


@app.route('/status/<task_id>')
def task_status(task_id):
    task = long_task.AsyncResult(task_id)

    response = {
        'state': task.state,
        'info': task.info,
    }

    if task.state == States.pending:
        response['status'] = 'Pending...'
    elif task.state == States.progress:
        response['status'] = 'In progress...'
    elif task.state == States.success:
        response['status'] = 'Success...'
    else:
        response['status'] = 'Unknown state?'
    return jsonify(response)