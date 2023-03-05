from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Student.query.get(int(id))

enrolled = db.Table('enrolled',
    db.Column('studentid', db.Integer, db.ForeignKey('student.id')),
    db.Column('classid', db.Integer, db.ForeignKey('class.id'))
)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  
    title = db.Column(db.String(150))
    major = db.Column(db.String(20), db.ForeignKey('major.name'))
    roster = db.relationship('Student', 
                             secondary=enrolled,
                             primaryjoin=(enrolled.c.classid == id),
                             lazy='dynamic', overlaps="classes")    
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
    classes = db.relationship('Class', 
                              secondary=enrolled,
                              primaryjoin=(enrolled.c.studentid == id),
                              lazy='dynamic', overlaps="roster")    

    def __repr__(self):
        return '<Student {} - {} {};>'.format(self.id,self.firstname, self.lastname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def enroll(self,newclass):
        if not self.is_enrolled(newclass):
            self.classes.append(newclass)

    def unenroll(self,newclass):
        if self.is_enrolled(newclass):
            self.classes.remove(newclass)

    def is_enrolled(self,newclass):
        return self.classes.filter(enrolled.c.classid == newclass.id).count() > 0

    # def enrolledCourses(self):
    #     return Class.query.join(enrolled, (enrolled.c.classid == Class.id)).filter(enrolled.c.studentid == self.id).order_by(Class.coursenum)

    def enrolledCourses(self):
        return self.classes