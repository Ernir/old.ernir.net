from flask.ext.wtf import Form
from wtforms import HiddenField, TextAreaField
from wtforms.validators import Required
from wtforms.widgets import TextArea


class LoginForm(Form):
    openid = HiddenField("openid", default="https://www.google.com/accounts/o8/id", validators=[Required()])


class CommentForm(Form):
    text = TextAreaField("content")


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()