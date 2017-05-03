# -*- encoding: utf-8

import os


SECRET_KEY = os.environ['FLASK_SECRET_KEY']

CELERY_BROKER_URL = os.environ.get(
    'CELERY_BROKER_URL', 'redis://localhost:6379/0'
)

CELERY_RESULT_BACKEND = os.environ.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'
)

TUMBLR_API_KEY = os.environ['TUMBLR_API_KEY']
