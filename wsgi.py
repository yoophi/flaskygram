import os

from flaskygram import create_app


app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    app.run()