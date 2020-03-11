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




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




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

class UserForm(FlaskForm):
    emailAddress = StringField('emailAddress', validators=[InputRequired(), Email(message='Invalid email'), Length(max=150)])
    userName = StringField('userName', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=150)])
    UserType=StringField('UserType', validators=[InputRequired(), Length(max=1)])



@app.route('/Register' ,methods=['GET', 'POST'], endpoint='Register')
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

