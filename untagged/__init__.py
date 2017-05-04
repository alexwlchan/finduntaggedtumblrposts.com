# -*- encoding: utf-8 -*-

from flask import Flask
from celery import Celery

from .tumblr import TumblrSession

app = Flask(__name__)
app.config.from_object('config')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

sess = TumblrSession(api_key=app.config['TUMBLR_API_KEY'])

from . import views  # noqa
