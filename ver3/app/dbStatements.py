from app import db
from app.models import Student, Class, Enrolled
from datetime import datetime

db.create_all()

c1 = Class(coursenum='322',major='CptS', title='Software Engineering')
c2 = Class(coursenum='355',major='CptS', title='Programming Languages')
c3 = Class(coursenum='451',major='CptS', title='Database Systems')

db.session.add(c1)
db.session.add(c2)
db.session.add(c3)
db.session.commit()

# add students
s1 = Student(username='sakire', firstname = 'Sakire', lastname = 'Arslan Ay', email='sakire@wsu.edu') 
s2 = Student(username='john', firstname = 'John', lastname = 'Yates', email='john@wsu.edu') 
db.session.add(s1)
db.session.add(s2)
db.session.commit()

s1 = Student.query.filter_by(username='sakire').first()
s2 = Student.query.filter_by(username='john').first()

c1 = Class.query.filter_by(coursenum='322').first()
c2 = Class.query.filter_by(coursenum='355').first()

#Enroll students in classes, i.e., add Class-Student associations
assoc1 = Enrolled(enrolldate=datetime.utcnow())
assoc1.classenrolled = c1
assoc1.studentenrolled = s1
db.session.add(assoc1)
db.session.commit()

assoc2 = Enrolled(enrolldate=datetime.utcnow())
assoc2.classenrolled = c2
s1.classes.append(assoc2)
db.session.commit()

assoc3 = Enrolled(classenrolled = c3, enrolldate=datetime.utcnow())
s1.classes.append(assoc3)
db.session.commit()

assoc4 = Enrolled(studentenrolled = s2, enrolldate=datetime.utcnow())
c1.roster.append(assoc4)
db.session.commit()

assoc5 = Enrolled(studentenrolled = s2)
c2.roster.append(assoc5)
db.session.commit()

assoc5 = Enrolled(studentenrolled = s2, classenrolled=c3)
db.session.add(assoc5)
db.session.commit()

for c in c1.roster:
    print(c)

for s in s1.classes:
    print(s)




