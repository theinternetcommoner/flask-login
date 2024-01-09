from flask import *
from functools import wraps
import sqlite3 as db

app = Flask(__name__)
app.secret_key = 'Secret!'

def login_required(f):
	@wraps(f)
	def _login_required(*args, **kwargs):
		if session.get('username'):
			return f(*args, **kwargs)
		else:
			return redirect(url_for('loginpage'))
	return _login_required

@app.route('/logincheck', methods = ['GET', 'POST'])
def logincheck():
	if request.method == 'POST':
		try:
			cn = db.connect('login.db')
			cur = cn.cursor()

			query = """
				SELECT * FROM tbl_login WHERE Username = ? AND Password = ?
			"""
			cur.execute(query, (request.form['username'], request.form['password']))

			rw = cur.fetchall()
			for x in rw:
				x
			session['username'] = x[1]
			return redirect(url_for('adminpage'))
		except:
			return redirect(url_for('loginpage'))
			# return '-1'

@app.route('/login')
def loginpage():
	return render_template('loginpage.html')

@app.route('/')
def homepage():
	session.pop('username', None)
	return render_template('index.html')

@app.route('/admin')
def adminpage():
	if 'username' in session:
		user = session['username']
		return render_template('adminpage.html', username = user)
	return redirect(url_for('loginpage'))

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('homepage'))

if __name__ == '__main__':
	app.run(debug = True)