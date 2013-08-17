from flask import Flask,render_template
 
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/oneAndHalfMileRunWalk')
def oneAndHalfMileRunWalk():
    return render_template("oneAndHalfMileRunWalk.html")

if __name__ == "__main__":
    app.run(debug = True) #We will set debug false in production 