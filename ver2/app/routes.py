from flask import render_template, flash, redirect, url_for, request
from app import app,db
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from app.forms import ClassForm, RegistrationForm, LoginForm, EditStudentForm
from app.models import Class, Major, Student

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Major.query.count() == 0:
        majors = [{'name':'CptS','department':'School of EECS'},{'name':'SE','department':'Schoolof EECS'},{'name':'EE','department':'School of EECS'},
                  {'name':'ME','department':'Mechanical Engineering'}, {'name':'MATH','department': 'Mathematics'}  ]
        for t in majors:
            db.session.add(Major(name=t['name'],department=t['department']))
        db.session.commit()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    classes = Class.query.order_by(Class.major).all()
    return render_template('index.html', title="Course List", classes = classes)

@app.route('/createclass/', methods=['GET', 'POST'])
@login_required
def createclass():
    form = ClassForm()
    if form.validate_on_submit():
        newClass = Class(coursenum = form.coursenum.data, title = form.title.data, major = form.major.data.name)
        db.session.add(newClass)
        db.session.commit()
        flash('Class "' + newClass.major + '-' + newClass.coursenum + '" is created')
        return redirect(url_for('index'))
    return render_template('create_class.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(username=form.username.data, email=form.email.data, firstname=form.firstname.data,lastname=form.lastname.data, address=form.address.data )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username=form.username.data).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/display_profile/', methods=['GET'])
@login_required
def display_profile():
    return render_template('display_profile.html', title='Display Profile',student=current_user)

@app.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditStudentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.firstname = form.firstname.data
            current_user.lastname = form.lastname.data
            current_user.address = form.address.data
            current_user.email = form.email.data
            current_user.set_password(form.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('display_profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',form=form)

@app.route('/roster/<classid>', methods=['GET'])
@login_required
def roster(classid):
    current_class = Class.query.filter_by(id=classid).first()
    return render_template('roster.html', title="Class Roster", current_class=current_class)