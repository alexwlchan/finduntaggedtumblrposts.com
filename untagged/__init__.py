#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import collections
import enum
import os

from flask import Flask, request, render_template, redirect, url_for, jsonify
from celery import Celery

from .tumblr import TumblrSession


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


try:
    api_key = os.environ['TUMBLR_API_KEY']
except KeyError:
    raise RuntimeError(
        "Couldn't find TUMBLR_API_KEY environment variable"
    ) from None
else:
    sess = TumblrSession(api_key=api_key)


Post = collections.namedtuple('Post', ['url', 'type', 'date'])


class States(enum.Enum):
    pending = 'PENDING'
    progress = 'PROGRESS'
    failure = 'FAILURE'


@celery.task(bind=True)
def long_task(self, hostname):
    """Background task that runs a long function with progress reports."""
    self.update_state(state=States.pending)

    # Make an initial request to the Tumblr API.  This checks that
    # our API key is correct and that the hostname exists.
    try:
        initial_resp = sess.get_posts(hostname=hostname)
    except RuntimeError as err:
        self.update_state(
            state=States.failure,
            meta={
                'message': err.args[0],
            }
        )
        return

    # If the initial request works, we can report the total posts
    # and the initial batch of untagged posts to the user.
    post_count = resp.post_count()
    posts = resp.untagged_posts()
    total_posts = resp.total_posts()
    self.update_state(
        state=States.progress,
        meta={
            'posts': posts,
            'post_count': post_count,
            'total_posts': total_posts,
        }
    )

    # Now fetch the remaining posts.  The Tumblr API doles out posts in
    # batches of 20.
    # TODO: This logic should be contained in tumblr.py, but I haven't
    # tidied it up yet.
    for offset in range(20, (post_count // 20) * 20, 20):
        try:
            resp = sess.get_posts(hostname=hostname, offset=offset)
        except RuntimeError as err:
            self.update_state(
                state=States.failure,
                meta={
                    'message': err.args[0],
                }
            )
            return

        post_count += resp.post_count()
        posts.extend(resp.untagged_posts())
        self.update_state(
            state=States.progress,
            meta={
                'posts': posts,
                'post_count': post_count,
                'total_posts': total_posts,
            }
        )

    return {
        'posts': posts,
        'post_count': post_count,
        'total_posts': total_posts,
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    hostname = request.args['hostname']
    task = long_task.apply_async((hostname, ))
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': None,
            'total': None,
            'posts': [],
            'status': 'Pending...'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 0),
            'posts': task.info.get('posts', []),
            'status': 'In progress...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 0),
            'posts': task.info.get('posts', []),
            'status': 'Success...'
        }
    else:
        # Something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return jsonify(response)
