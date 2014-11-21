# creates classes for db

from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nickname = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password = db.Column(db.String(12), index=True, unique = False)
  cases = db.relationship('Case', backref='case_lead', lazy='dynamic')

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    try:
      return unicode(self.id)  # python 2
    except NameError:
      return str(self.id)  # python 3

  def __repr__(self):
    return '<User %r>' % (self.nickname)

class Case(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  examinee = db.Column(db.String(140))
  start_date = db.Column(db.DateTime)
  primary_user = db.Column(db.Integer,db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Case %r>' % (self.examinee)