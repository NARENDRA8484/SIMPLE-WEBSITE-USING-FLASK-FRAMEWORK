from flask import Flask,render_template,redirect,url_for,request,flash
from db import Base,Register
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager,login_user,logout_user,current_user,login_required

app=Flask(__name__)

app.secret_key='1234'

login_manager=LoginManager(app)
login_manager.loginview='Login'
login_manager.login_message_category='Info'

@login_manager.user_loader
def load_user(user_id):
	return session.query(Register).get(int(user_id))

engine=create_engine('sqlite:///jntua.db',connect_args={'check_same_thread':False},echo=True)
DBsession=sessionmaker(bind=engine)
session=DBsession()
Base.metadata.bind=engine


@app.route("/")
def home():
	return render_template('INDEX1.html')
@app.route("/homepage")
def homepage():
	return render_template('HOMEPAGE.html')
@app.route("/register",methods=['GET','POST'])
def register():
	if request.method=="POST":
		newData=Register(name=request.form['name'],password=request.form['pwd'],phno=request.form['phno'],email=request.form['email'])
		session.add(newData)
		session.commit()
		return "Registration Successfully Completed"
		redirect(url_for('home'))
	return render_template('REGISTRATION FORM.html')
@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=='POST':
		email=request.form['email']
		password=request.form['pwd']
		user=session.query(Register).filter_by(email=email,password=password).one_or_none()
		if user==None:
			return render_template('loginunsuccess.html')
		login_user(user)
		flash("Login Success...")
		return redirect(url_for('homepage'))
	return render_template('LOGIN.html')

@app.route("/logout")
def logout():
	return redirect(url_for('home'))

@app.route("/viewusers")
def viewusers():
	dbData=session.query(Register).all()
	return render_template('viewusers.html',reg=dbData)


@app.route("/adminlogin",methods=['POST','GET'])
def adminlogin():
	if request.method=='POST':
		email=request.form['email']
		password=request.form['pwd']
		user=session.query(Register).filter_by(email=email,password=password).one_or_none()
		if user==None:
			flash("Login Unsuccessful!!!")
		login_user(user)
		return redirect(url_for('viewusers'))
	return render_template('adminlogin.html')

@app.route("/getstarted")
def getstarted():
	return render_template('getstarted.html')

@app.route('/deleteusers')
def home_function(): 
    dbData=session.query(Register).all()
    return render_template('delete.html',reg=dbData)

@app.route("/addusers",methods=['GET','POST'])
def addusers():
	if request.method=="POST":
		newData=Register(name=request.form['name'],password=request.form['pwd'],phno=request.form['phno'],email=request.form['email'])
		session.add(newData)
		session.commit()
		flash("USER SUCCESSFULLY ADDED")
		return redirect(url_for('viewusers'))
	return render_template('addusers.html')


@app.route("/voice")
def voice():
	return render_template('voice.html')

@app.route("/voice2")
def voice2():
	return render_template('voice2.html')


@app.route("/getlocation")
def getlocation():
	return render_template('geolocation.html')


@app.route("/admin")
def admin():
	return render_template('admin.html')






@app.route('/<int:register_id>/edit',methods=['GET','POST'])
def edit_function(register_id):
	editData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":
		editData.name=request.form['name']
		editData.email=request.form['email']
		session.add(editData)
		session.commit()
		flash("Data is updated")
		return redirect(url_for('viewusers'))
	return render_template('edit.html',register=editData)

@app.route('/<int:register_id>/delete',methods=['GET','POST'])
def delete_function(register_id):
	deleteData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":
		session.delete(deleteData)
		session.commit()
		flash("Data is deleted successfully....!")
		return redirect(url_for('viewusers'))
	return render_template('delete.html',register=deleteData)

app.run(debug=True,port=4000)