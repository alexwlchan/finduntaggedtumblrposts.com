#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import collections
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


def _extract_posts(resp):
    print(resp.json()['response']['posts'][0])
    return [
        Post(p['post_url'], p['type'], p['date'])
        for p in resp.json()['response']['posts'] if not p['tags']
    ]


@celery.task(bind=True)
def long_task(self, hostname):
    """Background task that runs a long function with progress reports."""
    resp = sess.get_posts(hostname=hostname)
    print(resp, resp.text[:200])

    self.update_state(state='PENDING')

    if resp.status_code != 200:
        self.update_state(
            state='FAILURE',
            meta={
                'status_code': resp.status_code,
                'message': resp.text,
            }
        )

    post_count = resp.json()['response']['total_posts']
    self.update_state(
        state='PROGRESS',
        meta={
            'total': post_count
        }
    )

    posts = _extract_posts(resp)
    self.update_state(
        state='PROGRESS',
        meta={
            'posts': posts,
            'current': len(resp.json()['response']['posts']),
            'total': post_count,
        }
    )

    for offset in range(20, (post_count // 20) * 20, 20):
        resp = sess.get_posts(hostname=hostname, offset=offset)
        print(resp, resp.text[:200])
        posts.extend(_extract_posts(resp))
        self.update_state(
            state='PROGRESS',
            meta={
                'posts': posts,
                'current': offset + 20,
                'total': post_count,
            }
        )

    return {
        'posts': posts,
        'current': post_count,
        'total': post_count,
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
