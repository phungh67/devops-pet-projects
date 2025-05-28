from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Hoang'}
    posts = [
        {
            'author': {'username': 'Hoang'},
            'body': 'Beautiful day in Sweden'
        },
        {
            'author': {'username': 'Skjord'},
            'body': 'Something to remember at MidSummer fest'
        }
    ]
    return render_template('index.html', title = 'Home', user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)