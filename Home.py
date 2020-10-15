from flask import Flask, render_template, redirect, url_for, session,request,g, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "VisiTia"
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
	conn = engine.connect()
	conn.execute('INSERT INTO users("name","pwd") VALUES("tia","tia")  ')
	conn.close()
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

"""
 db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	 return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/private')
@login_required
def private():
	conn = engine.connect ()
	users = conn.execute ('SELECT * FROM Users')
	resp = make_response (render_template("private.html",users = users ))
	conn.close ()
	return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


"""
