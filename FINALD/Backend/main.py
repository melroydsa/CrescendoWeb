from flask import Flask,redirect,render_template,flash,request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,LoginManager,login_manager,current_user

#db connection
local_server= True
app = Flask(__name__)
app.secret_key="Melroy"

#Unique User
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/student'
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(user_id)

class Testt(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))

class Students(UserMixin,db.Model):
    usn = db.Column(db.String(20),primary_key=True)
    user_id = db.Column(db.String(20))
    password = db.Column(db.String(20))
    Name = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(30))
    category = db.Column(db.String(10))
    def get_id(self):
           return (self.user_id)



@app.route("/")
def home():
    return render_template("Home.html")

@app.route('/Create',methods = ['POST','GET'])
def Create():
    if request.method=="POST":
        usn = request.form.get('usn')
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        Name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        category = request.form.get('category')
        new_user=db.engine.execute(f"INSERT INTO `students` (`USN`,`USER_ID`,`Password`,`Name`,`Phone`,`Email`,`Category`) VALUES ('{usn}','{user_id}','{password}','{Name}','{phone}','{email}','{category}')")
    return render_template("Create.html")

@app.route('/Login',methods = ['POST','GET'])
def Login():
    if request.method=="POST":
        user_id = request.form.get('user_id')
        password = request.form.get('Password')
        Student = Students.query.filter_by(user_id = user_id).first()
        if Student and password:
            login_user(Student)
            flash("SignIn Success")
        else:
            flash("Invalid Credentials","danger")
    return render_template("Login.html")
app.run(debug = True)