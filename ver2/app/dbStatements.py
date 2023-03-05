from app import db
from app.models import Student, Class, enrolled


c1 = Class.query.filter_by(coursenum = '321').filter_by(major='CptS').first()
c2 = Class.query.filter_by(coursenum = '322').filter_by(major='CptS').first()
c3 = Class.query.filter_by(coursenum = '355').filter_by(major='CptS').first()
c4 = Class.query.filter_by(coursenum = '451').filter_by(major='CptS').first()

s1 = Student.query.filter_by(username='sakire').first()

# Enroll student s1 in c2,c3,c4
s1.classes.append(c2)
s1.classes.append(c3)
s1.classes.append(c4)
db.session.commit()

# Unenroll student s1 from c4
s1.classes.remove(c4)
db.session.commit()

#retrive all classes a given student is enrolled in
#alternative1:
for c in s1.classes:
    print(c)

#alternative2:
enrolledClasses = Class.query.join(enrolled, (enrolled.c.classid == Class.id)).filter(enrolled.c.studentid == s1.id).order_by(Class.coursenum).all()

#check if the student is enrolled in a given class
s1.classes.filter(enrolled.c.classid == c2.id).count() > 0

#we can also add students to a class' roster
s2 = Student.query.filter_by(username='john').first()
c2.roster.append(s2)
db.session.commit()

for c in s2.classes:
    print(c)

for s in c2.roster:
    print(s)