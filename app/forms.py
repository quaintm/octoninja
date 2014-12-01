from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
  email = StringField('email', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  remember_me = BooleanField('remember_me', default=False)

  def validate(self):
    initial_validation = super(LoginForm, self).validate()

    if not initial_validation:
      return False

    self.email = User.query.filter_by(email=self.email.data).first()
    if not self.email:
      self.email.errors.append('Unknown Email')
      return False

    if not self.user.check_password(self.password.data):
      self.password.errors.append('Invalid password')
      return False

    if not self.user.active:
      self.username.errors.append('User not activated')
      return False

    return True