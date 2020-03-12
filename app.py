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



#AddNewItem

class Inventory(db.Model):
    idNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), unique=True)
    Description = db.Column(db.String(150))
    Price = db.Column(db.String(150))
    URL1=db.Column(db.String(1000))
    URL2=db.Column(db.String(1000))
    URL3=db.Column(db.String(1000))
    def get_id(self):
        return (self.idNo)


class InventoryForm(FlaskForm):
    options=StringField('options')
    Name = StringField('Name', validators=[InputRequired(), Length( max=20)])
    Description = StringField('Description', validators=[InputRequired(), Length( max=150)])
    Price = StringField('Price', validators=[InputRequired(), Length( max=150)])
    URL1  = FileField()
    URL2  = FileField()
    URL3 = FileField()
    

@app.route('/AddNewItem' , endpoint='AddNewItem'  ,methods=['GET', 'POST'])
@login_required
def AddNewItem():
    form=InventoryForm()
    if form.validate_on_submit():
        print("##########")        
        print(form.URL1)
        filename1 = secure_filename(form.URL1.data.filename)
        form.URL1.data.save('static/' + filename1)
        url1 =  filename1

        filename2 = secure_filename(form.URL2.data.filename)
        form.URL2.data.save('static/' + filename2)
        url2 =  filename2

        filename3 = secure_filename(form.URL3.data.filename)
        form.URL3.data.save('static/' + filename3)
        url3 =  filename3

        inv = Inventory(Name=form.Name.data, Description=form.Description.data, Price=form.Price.data,URL1=url1,URL2=url2,URL3=url3)
        db.session.add(inv)
        db.session.commit()
        return render_template('invAddSuccess.html')  
    
    return render_template('AddNewItem.html', form=form)




#ListAllItems

@app.route('/ListAllItems' , endpoint='ListAllItems'  ,methods=['GET', 'POST'])
@login_required
def ListAllItems():
    InventoryT = Inventory.query.all()
    return render_template('ListAllItems.html', InventoryT=InventoryT)


#/DeleteItem

class delInventoryForm(FlaskForm):
    options=StringField('options')

@app.route('/DeleteItem' , endpoint='DeleteItem'  ,methods=['GET', 'POST'])
@login_required
def DeleteItem():
    InventoryT = Inventory.query.all()
    form=delInventoryForm()
    print(form)
    print("$$$$$$$$$$$$"+str(form.options.data))
    if form.options.data!=None:
        print("##########")
        # print("$$$$$$$$$$$$"+form.options.data)
        print(form)
        Inventory.query.filter(Inventory.idNo == form.options.data).delete()
        db.session.commit()
        return render_template('deleteitemSuccess.html')
    return render_template('DeleteItem.html', InventoryT=InventoryT,form=form)


#/ShopProduct

class shopInventoryForm(FlaskForm):
    options=StringField('options')
    quantity=StringField('quantity')
    Price=StringField('quantity')

class OrderCart(db.Model):
    idNo = db.Column(db.Integer, primary_key=True)
    options = db.Column(db.String(150))
    quantity = db.Column(db.String(150))
    Price = db.Column(db.String(150))
    TotalPrice = db.Column(db.String(150))
    
@app.route('/ShopProduct' , endpoint='ShopProduct'  ,methods=['GET', 'POST'])
@login_required
def ShopProduct():
    form=shopInventoryForm()
    InventoryT = Inventory.query.all()
    if form.options.data!=None:
        print("form.Price.data"+form.Price.data)
        print("form.quantity.data"+form.quantity.data)
        Orders = OrderCart(options=form.options.data, quantity=form.quantity.data, Price=form.Price.data,TotalPrice=int(form.Price.data)*int(form.quantity.data))
        db.session.add(Orders)
        db.session.commit()
        return render_template('AdditionTocartSuccessful.html')
    return render_template('ShopProduct.html', InventoryT=InventoryT,form=form)



#/CheckoutCart

class orderForm(FlaskForm):
    options=StringField('options')
    quantity=StringField('quantity')
    Price=StringField('quantity')

    
class OrderList(db.Model):
    idNo = db.Column(db.Integer, primary_key=True)
    TotalPrice = db.Column(db.String(150))
    UserName = db.Column(db.String(150))
    

@app.route('/CheckoutCart' , endpoint='CheckoutCart'  ,methods=['GET', 'POST'])
@login_required
def CheckoutCart():
    form=orderForm()
    InventoryT = OrderCart.query.all()
    print(InventoryT)
    finalP=0
    for i in InventoryT:
        print(i.TotalPrice)
        finalP=finalP+int(i.TotalPrice)
    print(current_user)
    #if form!=None:
    if form.options.data!=None:
        Orderl = OrderList(TotalPrice=finalP, UserName=str(current_user))
#        OrderCart.query.delete()
        db.session.add(Orderl)
        db.session.query(OrderCart).delete()
        db.session.commit()
        return render_template('OrderSuccess.html')    


    return render_template('CheckoutCart.html', InventoryT=InventoryT,form=form)


#/MyOrders



@app.route('/MyOrders' , endpoint='MyOrders'  ,methods=['GET', 'POST'])
@login_required
def MyOrders():
    InventoryT = OrderList.query.all()
    
    return render_template('MyOrders.html', InventoryT=InventoryT)


