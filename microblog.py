from app import db

from app.models import User, Post

from app import cli, app_create

app = app_create()

cli.register(app)


@app.shell_context_processor

def make_shell_context():
    return {'db' : db, 'User': User, 'Post': Post}