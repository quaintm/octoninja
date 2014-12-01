from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
  UserMixin, RoleMixin, login_required
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# app import must happen last, after definitions
from app import views, models