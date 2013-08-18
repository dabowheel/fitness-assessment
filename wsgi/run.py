from flask import Flask,render_template,request,session,g,redirect,url_for,abort,flash
import sqlite3
from contextlib import closing
 
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    try:
        return sqlite3.connect("C:\\Users\\Miguel\\temp.db")
    except:
        return sqlite3.connect("/tmp/jobokugamen.db")
    if not hasTable():
        init_db()

def hasTable():
    cur = g.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entries'")
    return len(cur.fetchall()) > 0
    
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def showEntries():
    cur = g.db.execute('select sex,weight,weightUnit,mileTime,heartRate,vo2max from entries order by id desc')
    entries = [dict(sex=row[0], weight=row[1], weightUnit=row[2], mileTime=row[3], heartRate=row[4], vo2max=row[5]) for row in cur.fetchall()]
    return render_template("index.html",entries=entries,page="home")

@app.route('/Profile')
def profile():
    cur = g.db.execute('select sex,weight,weightUnit from profile order by id desc')
    profile = [dict(sex=row[0], weight=row[1], weightUnit=row[2]) for row in cur.fetchall()]
    return render_template("profile.html",profile=profile,page="profile")

@app.route('/Add', methods=['POST'])
def addEntry():
    if not session.get('logged_in'):
        abort(401)
    if len(request.form.getlist("weightUnit")) > 0:
        weightUnit = request.form.getlist("weightUnit")[0]
    else:
        weightUnit = ""
    g.db.execute('insert into entries (sex, weight, weightUnit, mileTime, heartRate, vo2max) values (?, ?, ?, ?, ?, ?)',
                 [request.form['sex'], request.form['weight'], weightUnit, request.form['time'], request.form['heartRate'], request.form['vo2max']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('showEntries'))

@app.route('/SaveProfile', methods=['POST'])
def saveProfile():
    if not session.get('logged_in'):
        abort(401)
    if len(request.form.getlist("weightUnit")) > 0:
        weightUnit = request.form.getlist("weightUnit")[0]
    else:
        weightUnit = ""
    g.db.execute('insert into profile (sex, weight, weightUnit) values (?, ?, ?)',
                 [request.form['sex'], request.form['weight'], weightUnit])
    g.db.commit()
    flash('Profile updated successfully')
    return redirect(url_for('showEntries'))

@app.route('/ClearUserData')
def clearUserData():
    if not session.get('logged_in'):
        abort(401)
    init_db()
    flash('User data cleared successfully')
    return redirect(url_for('showEntries'))    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('showEntries'))
    return render_template('login.html', error=error,page="login")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('showEntries'))

if __name__ == "__main__":
    app.run(debug = True) #We will set debug false in production 