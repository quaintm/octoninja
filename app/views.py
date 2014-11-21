# views -- defines each page route for the app

from flask import render_template, flash, redirect, session, urf_for,
  request, g
from flask.ext.login import login_user, logout_user, current_user, 
  login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User

@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'Will'} # fake user
  
  return render_template('index.html',
    title='Home', user=user)

@app.route('/login', methods=['GET','POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    return oid.try_login(form.openid.data, ask_for=['nickname','email'])

    # flash(('Login requested for UserID=%s, Password=%s, remember_me=%s') 
    #   % (str(form.userid.data), str(form.password.data), 
    #     str(form.remember_me.data)))
    # return redirect('/index')

  return render_template('login.html',
    title = 'Sign In', form=form)

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))