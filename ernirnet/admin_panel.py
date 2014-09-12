from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask.ext import login
from ernirnet.helpers.blog.blog_models import User, Tag, Comment, Blog
from ernirnet.helpers.blog.forms import CKTextAreaField
from ernirnet.helpers.bufftracker.spell_models import NumericalBonus, Spell, ModifierType, Statistic, NumericalBonus, MiscBonus, Source, StatisticsGroup
from ernirnet import app, db


class UserView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


class BlogView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1:
                return True
        return False

    create_template = "admin/edit.html"
    edit_template = "admin/edit.html"
    form_overrides = dict(body=CKTextAreaField)

    def __init__(self, session, **kwargs):
        super(BlogView, self).__init__(Blog, session, **kwargs)

class TagView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(TagView, self).__init__(Tag, session, **kwargs)


class CommentView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(CommentView, self).__init__(Comment, session, **kwargs)


class NumericalBonusView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(NumericalBonusView, self).__init__(NumericalBonus, session, **kwargs)


class MiscBonusView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(MiscBonusView, self).__init__(MiscBonus, session, **kwargs)

class SpellView(ModelView):

    column_exclude_list = ['real_spell']

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(SpellView, self).__init__(Spell, session, **kwargs)


class ModifierTypeView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(ModifierTypeView, self).__init__(ModifierType, session, **kwargs)


class StatisticView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(StatisticView, self).__init__(Statistic, session, **kwargs)


class SourceView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(SourceView, self).__init__(Source, session, **kwargs)


class StatisticsGroupView(ModelView):

    def is_accessible(self):
        if login.current_user.is_authenticated():
            if login.current_user.role == 1 or login.current_user.role == 2:
                return True
        return False

    def __init__(self, session, **kwargs):
        super(StatisticsGroupView, self).__init__(StatisticsGroup, session, **kwargs)

admin = Admin(app)

admin.add_view(UserView(db.session, endpoint="user"))

admin.add_view(BlogView(db.session, endpoint="blog", category="Blog"))
admin.add_view(TagView(db.session, endpoint="tag", category="Blog"))
admin.add_view(CommentView(db.session, endpoint="comment", category="Blog"))

admin.add_view(SpellView(db.session, endpoint="spell"))

admin.add_view(NumericalBonusView(db.session, endpoint="numerical-bonus", category="Bonus"))
admin.add_view(MiscBonusView(db.session, endpoint="misc-bonus", category="Bonus"))

admin.add_view(StatisticView(db.session, endpoint="statistic", category="Other"))
admin.add_view(ModifierTypeView(db.session, endpoint="modifer-type", category="Other"))
admin.add_view(StatisticsGroupView(db.session, endpoint="statistic-group", category="Other"))
admin.add_view(SourceView(db.session, endpoint="source", category="Other"))