from flask import render_template, flash, redirect, url_for, request
import requests
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home/')
def home():
    url = "https://api.betaseries.com/shows/random"
    querystring = {"key":"7c2f686dfaad","v":"3.0","nb":"3"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    for post in posts:
        if len(post["description"]) > 500:
            post["description"] = post["description"][:500] + "..."
    return render_template('home.html', posts=posts, bonjour="eh non")

@app.route('/series/<starting>/<int:page>/')
def series(starting, page):
    url = "https://api.betaseries.com/shows/list"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "order": "alphabetical", "limit": "9", "starting": starting,
                   "start": (page-1)*9, "fields": "id,title,images.show"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    for post in posts:
        if len(post.keys()) == 2:
            post['images'] = {'show': url_for('static', filename='img/logo.png')}
    return render_template('series.html', posts=posts, starting=starting, page=page)

@app.route('/serie/<int:serie_id>/')
def serie(serie_id):
    url = "https://api.betaseries.com/shows/episodes"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "id":serie_id}
    episodes = requests.request("GET", url, params=querystring).json()["episodes"]
    url2 = "https://api.betaseries.com/shows/seasons"
    saisons = requests.request("GET", url2, params=querystring).json()["seasons"]
    url3 = "https://api.betaseries.com/shows/display"
    display = requests.request("GET", url3, params=querystring).json()["show"]
    return render_template('serie.html', episodes=episodes, saisons=saisons, display=display)

@app.route('/my_list/<starting>/<int:page>/')
@login_required
def my_list(starting, page):
    url = "https://api.betaseries.com/shows/list"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "order": "alphabetical", "limit": "9", "starting": starting,
                   "start": (page-1)*9, "fields": "id,title,images.show"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    for post in posts:
        if len(post.keys()) == 2:
            post['images'] = {'show': url_for('static', filename='img/logo.png')}
    return render_template('series.html', posts=posts, starting=starting, page=page)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)