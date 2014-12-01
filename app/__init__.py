from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import basedir
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
import os

app = Flask(__name__)
app.config.from_object('config')



db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# commands for flask-migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

# app import must happen last, after definitions
from app import views, models