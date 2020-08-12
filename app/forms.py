import wtforms
from wtforms import validators
from models import User

class LoginForm(wtforms.Form):
  username = wtforms.StringField("Username",
    validators=[validators.DataRequired()])
  password = wtforms.PasswordField("Password",
    validators=[validators.DataRequired()])
  remember_me = wtforms.BooleanField("Remember me?",
    default=True)

  def validate(self):
    if not super(LoginForm, self).validate():
      return False

    self.user = User.authenticate(self.username.data, self.password.data)
    if not self.user:
      self.username.errors.append("Invalid username or password")
      return False

    return True