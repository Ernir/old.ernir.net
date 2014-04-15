from flask.ext.wtf import Form
from wtforms import HiddenField
from wtforms.validators import Required


class LoginForm(Form):
    openid = HiddenField('openid', default="https://www.google.com/accounts/o8/id", validators=[Required()])