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

def hasTable():
    cur = g.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entries'")
    rows = cur.fetchall()
    res = [dict(name=row[0]) for row in rows]
    return len(rows)>0
    
def init_db():
    with app.open_resource('schema.sql', mode='r') as f:
        g.db.cursor().executescript(f.read())
    g.db.commit()
        
@app.before_request
def before_request():
    g.db = connect_db()
    if not hasTable():
        init_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def showEntries():
    profile = getProfile()
    if profile == None or profile['sex'] == "" or profile['weight'] == "" or profile['weightUnit'] == "":
        return redirect(url_for('profile'))
    cur = g.db.execute('select weight,weightUnit,mileTime,heartRate,vo2max from entries order by id desc')
    entries = [dict(weight=row[0], weightUnit=row[1], mileTime=row[2], heartRate=row[3], vo2max=row[4]) for row in cur.fetchall()]
    return render_template("index.html",profile=profile,entries=entries,page="home")

@app.route('/Profile')
def profile():
    profile = getProfile()
    return render_template("profile.html",profile=profile,page="profile")

def getProfile():
    cur = g.db.execute('select sex,weight,weightUnit from profile where id=1 order by id desc')
    row = cur.fetchone()
    if row == None:
        return None
    else:
        return dict(sex=row[0], weight=row[1], weightUnit=row[2])
    
def updateProfile(sex,weight,weightUnit):
    g.db.execute('update profile set sex=?, weight=?, weightUnit=? where id=1', [sex, weight, weightUnit])
    g.db.commit()
    
def insertProfile(sex,weight,weightUnit):
    g.db.execute('insert into profile (sex, weight, weightUnit) values (?, ?, ?)', [sex, weight, weightUnit])
    g.db.commit()

@app.route('/Add', methods=['POST'])
def addEntry():
    if not session.get('logged_in'):
        abort(401)
    if len(request.form.getlist("weightUnit")) > 0:
        weightUnit = request.form.getlist("weightUnit")[0]
    else:
        weightUnit = ""
    g.db.execute('insert into entries (weight, weightUnit, mileTime, heartRate, vo2max) values (?, ?, ?, ?, ?)',
                 [request.form['weight'], weightUnit, request.form['time'], request.form['heartRate'], request.form['vo2max']])
    g.db.commit()
    profile = getProfile()
    updateProfile(profile['sex'],request.form['weight'],request.form['weightUnit'])
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
    if getProfile() == None:
        insertProfile(request.form['sex'],request.form['weight'],weightUnit)
    else:
        updateProfile(request.form['sex'],request.form['weight'],weightUnit)
        
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