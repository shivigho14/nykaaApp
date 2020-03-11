from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, PasswordField, BooleanField
from flask_bootstrap import Bootstrap
from wtforms.validators import InputRequired, Email, Length

from flask_wtf import FlaskForm 
from flask_sqlalchemy  import SQLAlchemy

from flask_wtf.file import FileField
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import os

## Configurations below

app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'secretgey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


#routing starts

@app.route('/')
def index():
	#return '<h1>Hello!</h1>'
	return render_template('Welcome.html')#, form=form)








@app.route('/WelcomePage', endpoint='WelcomePage')
def WelcomePage():
	#return '<h1>Hello!</h1>'
	return render_template('Welcome.html')#, form=form)


###table definition

class User(UserMixin, db.Model):
    idNo = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True)
    emailAddress = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    UserType=db.Column(db.String(1))
    def get_id(self):
        return (self.idNo)

class UserForm(FlaskForm):
    emailAddress = StringField('emailAddress', validators=[InputRequired(), Email(message='Invalid email'), Length(max=150)])
    userName = StringField('userName', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=150)])
    UserType=StringField('UserType', validators=[InputRequired(), Length(max=1)])



@app.route('/Register', endpoint='Register' ,methods=['GET', 'POST'])
def Register():
    #return '<h1>Hello!</h1>'
    form =UserForm()
    if form.validate_on_submit():
        
        sha256_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(userName=form.userName.data, emailAddress=form.emailAddress.data, password=sha256_password,UserType=form.UserType.data)
        db.session.add(new_user)
        db.session.commit()
        return render_template('RegisterSuccess.html')
    return render_template('Register.html', form=form)





#ListAllUsers

@app.route('/ListAllUsers', endpoint='ListAllUsers' ,methods=['GET', 'POST'])
#@login_required
def ListAllUsers():
    UserTable = User.query.all()
    return render_template('ListAllUsers.html', UserTable=UserTable)
    #return render_template('ListAllUsers.html')#, form=form)

class loginForm(FlaskForm):
    
    userName = StringField('userName', validators=[InputRequired(), Length( max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length( max=150)])
    remember = BooleanField('remember me')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#/login
@app.route('/login', endpoint='login'  ,methods=['GET', 'POST'])
#@login_required
def login():
    form =loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(userName=form.userName.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return render_template('loginsuccessful.html')
        return render_template('loginUnsuccessful.html')
    
    
    return render_template('login.html', form=form)



#/logout

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('Welcome.html')#, form=form)






