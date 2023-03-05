from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Student.query.get(int(id))

#https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html 

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  
    title = db.Column(db.String(150))
    major = db.Column(db.String(20), db.ForeignKey('major.name'))
    roster = db.relationship('Enrolled',back_populates='classenrolled') 
  
    def __repr__(self):
        return '<Class {}{}-{} >'.format(self.major,self.coursenum,self.title)
    def getTitle(self):
        return self.title

class Major(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    department = db.Column(db.String(150))
    classes = db.relationship('Class', backref='coursemajor', lazy='dynamic')
    def __repr__(self):
        return '<Major {}-{} >'.format(self.name,self.department)
    
class Student(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    address = db.Column(db.String(200))
    email = db.Column(db.String(120), index=True, unique=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    classes = db.relationship('Enrolled',back_populates='studentenrolled') 

    def __repr__(self):
        return '<Student {} - {} {};>'.format(self.id,self.firstname, self.lastname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def enroll(self,newclass):
        if not self.is_enrolled(newclass):
            # create a new Enrolled instance for the 'newclass' and append it to the current enrolled classes of the student
            newEnrollment = Enrolled(studentenrolled =  self, classenrolled = newclass)
            self.classes.append(newEnrollment)
            db.session.commit()

    def unenroll(self,theclass):
        if self.is_enrolled(theclass):
            curEnrollment = Enrolled.query.filter_by(studentid=self.id).filter_by(classid=theclass.id).first()
            db.session.delete(curEnrollment)
            db.session.commit()

    def is_enrolled(self,theclass):
        return Enrolled.query.filter_by(studentid=self.id).filter_by(classid=theclass.id).count() > 0

    def getEnrolmentDate(self, theclass):
        if self.is_enrolled(theclass):
            return Enrolled.query.filter_by(studentid=self.id).filter_by(classid=theclass.id).first().enrolldate
        else:
            return None 

    def enrolledCourses(self):
        return self.classes

class Enrolled(db.Model):
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)
    enrolldate = db.Column(db.DateTime, default=datetime.utcnow)
    studentenrolled = db.relationship('Student')
    classenrolled = db.relationship('Class')

