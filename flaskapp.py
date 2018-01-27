#!/usr/bin/env python
# -*- encoding: utf-8

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to Find Untagged Tumblr Posts!'


if __name__ == '__main__':
    app.run(debug=True)
