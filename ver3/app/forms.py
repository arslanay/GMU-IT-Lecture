from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import  ValidationError, DataRequired, Email, EqualTo, Length
from app.models import Class, Major, Student
from flask_login import current_user

def get_major():
    return Major.query

class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    title =  StringField('Course Title', validators=[DataRequired()])
    major = QuerySelectField('Majors', query_factory = get_major, get_label='name', allow_blank=False)
    submit = SubmitField('Post')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address =  TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        student = Student.query.filter_by(username=username.data).first()
        if student is not None:
            raise ValidationError('The username already exists! Please use a different username.')

    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student is not None:
            raise ValidationError('The email already exists! Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EditStudentForm(FlaskForm):
    firstname =  StringField('Firstname', validators=[DataRequired()])
    lastname =  StringField('Firstname', validators=[DataRequired()])
    address = TextAreaField('Address',[Length(min=0, max=200)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])    
    submit = SubmitField('Submit')
    
    def validate_email(self, email):
        students = Student.query.filter_by(email=email.data).all()
        for  student in students:
            if (student.id != current_user.id):
                raise ValidationError('The email is already associated with another account! Please use a different email address.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')    

#More information about WTForms validators https://wtforms.readthedocs.io/en/2.3.x/validators/

