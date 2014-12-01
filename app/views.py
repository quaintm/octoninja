# views -- defines each page route for the app

from flask import (
  render_template, 
  flash, 
  redirect, 
  session, 
  url_for,
  request, 
  g)
from flask.ext.login import (
  login_user, 
  logout_user, 
  current_user, 
  login_required)
from flask.ext.security import (
  Security, 
  SQLAlchemyUserDatastore,
  UserMixin, 
  RoleMixin, 
  login_required)
from flask.ext.security.utils import encrypt_password
from app import app, db, lm, oid
from forms import LoginForm
from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# pre-load actions
@lm.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.before_first_request
def create_user():
    db.create_all()
    user = User.query.first()
    if user is None:
      user_datastore.create_user(
        nickname='Monica',
        email='quaintm@email.net', 
        password=encrypt_password('password'))
    db.session.commit()

@app.before_request
def before_request():
  g.user = current_user


#routes
@app.route('/')
@app.route('/index')
@login_required
def index():
  user = g.user
  return render_template('index.html',
    title='Home', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('index'))
  form = LoginForm(request.form)
  if request.method == 'POST':
    if form.validate_on_submit():
      login_user(form.email)
      flash("Login Successful")
      session['remember_me'] = form.remember_me.data
      redirect_url = request.args.get("next") or url_for("index")
      return redirect(redirect_url)

    else:
      flash_errors(form)
  return render_template('login.html',
    title = 'Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

