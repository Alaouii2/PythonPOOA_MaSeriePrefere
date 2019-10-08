from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/series/')
def series():
    return render_template('series.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/game-single/')
def gamesingle():
    return render_template('game-single.html')

@app.route('/register/')
def register():
    return render_template('register.html')

# @app.route('/contents/<int:content_id>/')
# def content(content_id):
#     return '%s' % content_id
