# views -- defines each page route for the app

from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'Will'} # fake user
  
  return render_template('index.html',
    title='Home', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash(('Login requested for UserID=%s, Password=%s, remember_me=%s') 
      % (str(form.userid.data), str(form.password.data), 
        str(form.remember_me.data)))
    return redirect('/index')
  return render_template('login.html',
    title = 'Sign In', form=form)