import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(current_dir, 'database.sqlite3')}"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roll_number = db.Column(db.String, unique=True, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String)
  courses = db.relationship("Course",
                            backref="students",
                            secondary="enrollments")


class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_name = db.Column(db.String, nullable=False)
  course_description = db.Column(db.String)
  student = db.relationship("Student", secondary="enrollments")


class Enrollments(db.Model):
  __tablename__ = "enrollments"
  enrollment_id = db.Column(db.Integer, primary_key=True, nullable=False)
  estudent_id = db.Column(db.Integer,
                          db.ForeignKey("student.student_id"),
                          nullable=False)
  ecourse_id = db.Column(db.Integer,
                         db.ForeignKey("course.course_id"),
                         nullable=False)


@app.route('/')
def index():
  all_students = Student.query.all()
  return render_template('index.html', all_students=all_students)


@app.route('/student/create', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('form.html')
  if request.method == 'POST':
    roll, f_name, l_name = request.form.get('roll'), request.form.get(
        'f_name'), request.form.get('l_name')
    courses_list = request.form.getlist('courses')
    if bool(Student.query.filter_by(roll_number=roll).first()):
      return render_template('already_exist.html')
    else:
      stud = Student(roll_number=roll, first_name=f_name, last_name=l_name)
      for subject in courses_list:
        subject_obj = Course.query.filter_by(course_id=int(subject[-1])).one()
        stud.courses.append(subject_obj)
      db.session.add(stud)
      db.session.commit()
      return redirect('/')


@app.route('/student/<int:student_id>')
def details(student_id):
  st = Student.query.filter_by(student_id=student_id).one()
  cl = st.courses
  return render_template('personal_details.html', st=st, cl=cl)


@app.route('/student/<int:student_id>/delete')
def delete(student_id):
  db.session.delete(Student.query.filter_by(student_id=student_id).one())
  db.session.commit()
  return redirect('/')


@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
  stu = Student.query.filter_by(student_id=student_id).one()
  stu.courses = []
  if request.method == 'POST':
    new_fname, new_lname, new_courses = request.form.get(
        'f_name'), request.form.get('l_name'), request.form.getlist('courses')
    stu.first_name = new_fname
    stu.last_name = new_lname
    for new_c in new_courses:
      c_obj = Course.query.filter_by(course_id=int(new_c[-1])).one()
      stu.courses.append(c_obj)
    db.session.commit()
    return redirect('/')
  else:
    return render_template('update_details.html', stu=stu)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(current_dir, 'database.sqlite3')}"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Student(db.Model):
  __tablename__ = "student"
  student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  roll_number = db.Column(db.String, unique=True, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String)
  courses = db.relationship("Course",
                            backref="students",
                            secondary="enrollments")


class Course(db.Model):
  __tablename__ = "course"
  course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_name = db.Column(db.String, nullable=False)
  course_description = db.Column(db.String)
  student = db.relationship("Student", secondary="enrollments")


class Enrollments(db.Model):
  __tablename__ = "enrollments"
  enrollment_id = db.Column(db.Integer, primary_key=True, nullable=False)
  estudent_id = db.Column(db.Integer,
                          db.ForeignKey("student.student_id"),
                          nullable=False)
  ecourse_id = db.Column(db.Integer,
                         db.ForeignKey("course.course_id"),
                         nullable=False)


@app.route('/')
def index():
  all_students = Student.query.all()
  return render_template('index.html', all_students=all_students)


@app.route('/student/create', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('form.html')
  if request.method == 'POST':
    roll, f_name, l_name = request.form.get('roll'), request.form.get(
        'f_name'), request.form.get('l_name')
    courses_list = request.form.getlist('courses')
    if bool(Student.query.filter_by(roll_number=roll).first()):
      return render_template('already_exist.html')
    else:
      stud = Student(roll_number=roll, first_name=f_name, last_name=l_name)
      for subject in courses_list:
        subject_obj = Course.query.filter_by(course_id=int(subject[-1])).one()
        stud.courses.append(subject_obj)
      db.session.add(stud)
      db.session.commit()
      return redirect('/')

@app.route('/student/<int:student_id>')
def details(student_id):
  st = Student.query.filter_by(student_id=student_id).one()
  cl = st.courses
  return render_template('personal_details.html', st=st, cl=cl)


@app.route('/student/<int:student_id>/delete')
def delete(student_id):
  db.session.delete(Student.query.filter_by(student_id=student_id).one())
  db.session.commit()
  return redirect('/')


@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
  stu = Student.query.filter_by(student_id=student_id).one()
  stu.courses = []
  if request.method == 'POST':
    new_fname, new_lname, new_courses = request.form.get(
        'f_name'), request.form.get('l_name'), request.form.getlist('courses')
    stu.first_name = new_fname
    stu.last_name = new_lname
    for new_c in new_courses:
      c_obj = Course.query.filter_by(course_id=int(new_c[-1])).one()
      stu.courses.append(c_obj)
    db.session.commit()
    return redirect('/')
  else:
    return render_template('update_details.html', stu=stu)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
