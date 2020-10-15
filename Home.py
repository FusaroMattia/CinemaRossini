from flask import Flask, render_template, redirect, url_for, session,request,g, request,Blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///:memory'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY'] = "VisiTia"
db = SQLAlchemy(app)
engine = create_engine('sqlite:///:memory', echo = True)
login_manager = LoginManager()
login_manager.init_app(app)



class User(UserMixin):
    def __init__(self,id,name,pwd):
    	self.id = id
    	self.name = name
    	self.pwd = pwd





@login_manager.user_loader
def load_user(user_id):
	conn = engine.connect()
	rs = conn.execute('SELECT * FROM users WHERE id = ?', user_id)
	user = rs.fetchone()
	conn.close()
	return User(user.id , user.name , user.pwd)


@app.route('/')
def home():
	if (current_user.is_authenticated):
		return render_template("index.html", cont = current_user.id)
	return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == "POST":
		conn = engine.connect()
		rs = conn.execute('SELECT pwd FROM users WHERE name = ?',[request.form['user']])
		real_psw = rs.fetchone()['pwd']
		if(request.form['pwd'] == real_psw):
			user = request.form['user']
			login_user(user)
		return redirect(url_for("private"))
	else:
		return render_template("login.html")

@app.route('/private')
@login_required
def private():
	conn = engine.connect()
	users = conn.execute('SELECT * FROM users')
	resp= make_response(render_template("private.html", users = users))
	conn.close()
	return resp

if __name__ == "__main__":
	app.run()
