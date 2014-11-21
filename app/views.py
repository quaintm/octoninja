# views -- defines each page route for the app

from flask import render_template, flash, redirect, session, urf_for,
  request, g
from flask.ext.login import login_user, logout_user, current_user, 
  login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
  user = {'nickname': 'Will'} # fake user
  
  return render_template('index.html',
    title='Home', user=user)

@app.before_request
def befire_request():
  g.user = current_user

@app.route('/login', methods=['GET','POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    return oid.try_login(form.userid.data, ask_for=['nickname','email'])

    # flash(('Login requested for UserID=%s, Password=%s, remember_me=%s') 
    #   % (str(form.userid.data), str(form.password.data), 
    #     str(form.remember_me.data)))
    # return redirect('/index')

  return render_template('login.html',
    title = 'Sign In', form=form,
    providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
  if resp.email is None or resp.email == "":
    flash('Invalid login.')
    return redirect(url_for('login'))
  user = User.query.filter_by(email=resp.email).first()
  if user is None:
    nickname = resp.nickname
    if nickname is None or nickname == "":
      nickname = resp.email.split('@')[0]
    user = User(nickname = nickname, email = resp.email)
    db.session.add(user)
    db.session.commit()
  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me',None)
  login_user(user, remember = remember_me)
  return rediredct(request.args.get('next') or url_for('index'))



