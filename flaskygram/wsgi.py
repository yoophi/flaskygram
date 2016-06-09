#!/usr/bin/env python
# coding: utf-8

import os

import markwiki
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from flaskygram import create_app

os.environ['MARKWIKI_HOME'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')

application = DispatcherMiddleware(
    create_app(os.getenv('FLASK_CONFIG') or 'default'),
    {'/docs': markwiki.app}
)

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True)
