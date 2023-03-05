from app import app, db

from app.models import Class, Major, Student

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Class': Class, 'Major': Major}

