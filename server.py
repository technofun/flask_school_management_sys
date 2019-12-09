from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(25)

# --------------database configueration---------------
project_dir = os.path.dirname(os.path.abspath(__file__))
dataBase_file = "sqlite:///{}".format(
    os.path.join(project_dir, "School_M_S.db"))

app.config['SQLALCHEMY_DATABASE_URI'] = dataBase_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --------------------Database Model / Records -----------------

# db.create_all()
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userName = db.Column(db.String(30), unique=False, nullable=False)
    mobile = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    joining_date = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    studentName = db.Column(db.String(30), unique=False, nullable=False)
    rollNumber = db.Column(db.Integer, unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    joining_date = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    email = db.Column(db.String(120), primary_key=True, unique=True)
    password = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id
# db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session.pop('admin', None)
        if request.form['login_password'] == 'admin':
            session['admin'] = request.form['login_email']
            return redirect('/admin')

    return render_template('adminLogin.html')


@app.before_request
def before_request():
    g.admin = None
    if 'admin' in session:
        g.admin = session['admin']


# @app.route('/admin', methods=['GET', 'POST'])
# def adminLogin():
#     if request.method == 'POST':
#         # adminUser = Admin.query.order_by(Admin.email).all()
#         # try:
#         #     if adminUser.email == 'admin@123.com' and adminUser.password == 'admin1234':
#         #         return redirect('/register')
#         #     else:
#         #         return 'incorrect pass'

#         # except:
#         #     return 'METHOD NOT POST'

#         # return redirect('/register')
#         # myadmin = Admin()
#         adminemail = request.form['login_email']
#         adminpassword = request.form['login_password']

#         # try:
#         # db.session.add(myadmin)
#         # db.session.commit()
#         # adminUser = Admin.query.order_by(Admin.email).first()
#         if adminemail == 'admin@123.com' and adminpassword == 'admin':
#             return redirect('/register')
#         # except:
#         #     return 'you are not Admin'

#         else:
#             return redirect('/')

#         return 'method is not post 2ND'


@app.route('/addteacher')
def addteacher():
    if g.admin:
        return render_template('addTeacher.html')
    return redirect(url_for('home'))


@app.route('/addstudent')
def addstudent():
    if g.admin:
        return render_template('addStudent.html')
    return redirect(url_for('home'))


@app.route('/admin')
def WelcomeAdmin():
    if g.admin:
        return render_template('welcomeAdmin.html')
    return redirect(url_for('home'))


@app.route('/teacher')
def teacher():
    return render_template('WelcomeTeacher.html')


# -------------- Show All users Teacher or Students-----------------
@app.route('/allstudents')
def allStudents():
    _students = Student.query.order_by(Student.id).all()
    return render_template('all_students_admin.html', _students=_students)

@app.route('/allteachers')
def allTeachers():
    _teachers = Users.query.order_by(Users.id).all()
    return render_template('all_teachers_admin.html', _teachers=_teachers)


# -------------Add Teacher Route ----------------------
@app.route('/admin/addTeacher', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        myteacher = Users()

        myteacher.userName = request.form['Username']
        myteacher.mobile = request.form['cell_no']
        myteacher.email = request.form['email']
        myteacher.password = request.form['password']
        myteacher.gender = request.form['gender']
        try:
            db.session.add(myteacher)
            db.session.commit()
            return redirect('/addteacher')
        except:
            return 'Not getting data from html form'

    else:
        return "<h1>method not post</h1>"


@app.route('/admin/addStudent', methods=['POST', 'GET'])
def student():
    if request.method == 'POST':
        mystudent = Student()

        mystudent.studentName = request.form['StudentName']
        mystudent.rollNumber = request.form['RollNumber']
        mystudent.mobile = request.form['cell_no']
        mystudent.email = request.form['email']
        mystudent.password = request.form['password']
        mystudent.gender = request.form['gender']
        db.session.add(mystudent)
        db.session.commit()
        return redirect('/addstudent')

    return "<h1>method not post</h1>"


@app.route('/teacher/students')
def allstudents():
    students = Users.query.order_by(Users.id).all()
    return render_template('showAllStudents.html', students=students)


#  --------------delete the user---------
@app.route('/delete/<int:id>')
def deleteStudent(id):
    user_to_delete = Student.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/allstudents')
    except:
        return 'user cant delete'

@app.route('/delete/<int:id>')
def deletTeacher(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/allteachers')
    except:
        return 'user cant delete'


if __name__ == '__main__':
    app.run(debug=True)
