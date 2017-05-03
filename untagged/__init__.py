# -*- encoding: utf-8 -*-

import os

from flask import Flask
from celery import Celery

from .tumblr import TumblrSession


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'sekrit-key')

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

from . import views
