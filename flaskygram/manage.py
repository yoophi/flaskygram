#!/usr/bin/env python

from __future__ import print_function

# Set the path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from flask_script.commands import Shell, ShowUrls
from flask_migrate import MigrateCommand, Migrate

from flaskygram import create_app
from flaskygram.database import db

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='sample/*')
    COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def test(coverage=False):
    """Run the unit test."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys

        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % (covdir,))
        COV.erase()


# Turn on debugger by default and reloader
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True, host='0.0.0.0'))

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('show_urls', ShowUrls)

from flaskygram.core.accounts.commands import *

if __name__ == "__main__":
    manager.run()
