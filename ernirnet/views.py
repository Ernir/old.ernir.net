from flask import render_template, jsonify, request, flash, redirect, g, url_for, session
from flask_login import login_user, logout_user, current_user, login_required

from ernirnet import app, lm, oid, db
from ernirnet.helpers.blog.blog_models import role_user, Blog, Tag, Comment
from ernirnet.helpers.blog.blog_models import User
from ernirnet.helpers.blog.forms import LoginForm, CommentForm
from ernirnet.helpers.bufftracker import spell_models
from ernirnet.helpers.bufftracker.xml_parse import Parser
from ernirnet.helpers.errors import InvalidUsage


'''
Main pages
'''


@app.route("/")
def home():
    return render_template("index.jinja2", sitename=u"Home")


@app.route("/CV/")
def cv():
    return render_template("cv.jinja2", sitename=u"CV")


@app.route("/contact/")
def contact():
    return render_template("contact.jinja2", sitename=u"Contact")


@app.route("/blog/")
def blog():
    posts = Blog.get_by_date()
    tags = Tag.get_by_usage()

    return render_template("blog.jinja2", sitename=u"Blog", posts=posts, tags=tags)


@app.route("/blog/<blog_url>/", methods=["GET", "POST"])
def individual_blog(blog_url):
    blog = Blog.get_by_url(blog_url)
    tags = Tag.get_by_usage()

    form = CommentForm()
    logged_in = g.user.is_authenticated()

    if request.method == "POST":
        Comment.commit(int(request.form["blog-id"]), request.form["text"], g.user)

    return render_template("blog.jinja2", sitename=u"Blog", posts=blog, tags=tags, logged_in=logged_in, form=form)


@app.route("/blog/tags/<tag_name>/")
def tagged_blogs(tag_name):
    blogs = Blog.get_by_tag(tag_name)
    tags = Tag.get_by_usage()

    return render_template("blog.jinja2", sitename=u"Blog", posts=blogs, tags=tags)


@app.route("/admin/delete/comment/", methods=["POST"])
@login_required
def delete_comment():
    if g.user.role == 1:
        Comment.delete(request.form["id"])
        return jsonify(status="OK")
    else:
        pass  # TODO: Handle unauthorized deletions

'''
Admin and login
'''


@app.route("/oldadmin/")
@login_required
def admin():
    if g.user.role == 1:
        comments = Comment.get_by_date()
        return render_template("admin.jinja2", sitename=u"Admin", comments=comments)
    else:
        return redirect(url_for("login"))


@lm.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route("/login", methods=["GET", "POST"])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        return oid.try_login(form.openid.data, ask_for=["nickname", "email"])
    return render_template("login.jinja2", sitename=u"Login", form=form)


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash("Invalid login. Please try again.")
        return redirect(url_for("login"))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, role=role_user)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(request.args.get("next") or url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("home"))


'''
Hobby subpages
'''


@app.route("/vanciantopsionics/")
def vtp():
    from ernirnet.helpers.vtp import get_old_vtp_files

    files = get_old_vtp_files()

    return render_template("vtp.jinja2", sitename=u"The Vancian to Psionics Project", old_files=files)


@app.route("/bufftracker/")
def buff_tracker():
    spell_list = spell_models.Spell.get_all_as_list()

    return render_template("bufftracker.jinja2", spell_list=spell_list, sitename=u"D&D 3.5 Buff Tracker")


'''
API routes
'''


@app.route("/api/parseMW/")
def mw_parse_api():
    sheet_id = request.args.get("id", 0, type=int)

    try:
        data = Parser().get_mw_data(sheet_id)
    except:
        raise InvalidUsage("No Myth-Weavers sheet with the given ID was found", status_code=400)
    return jsonify(data)

@app.route("/api/bufftracker/bonuses/", methods=["POST"])
def buff_tracker_new_bonuses_calculation():

    if request.method == "POST":
        cl_dictionary = request.get_json(force=True)

        numerical_bonuses = spell_models.NumericalBonus.get_applicable_as_dict_detailed(cl_dictionary)

        selected_spell_ids = [key for key in cl_dictionary]
        misc_bonuses = spell_models.MiscBonus.get_applicable_as_list(selected_spell_ids)

        content = dict(numerical=numerical_bonuses, misc=misc_bonuses)
        response = dict(content=content, status=200, message="OK")

        return jsonify(response)

@app.route("/api/bufftracker/statistics/")
def buff_tracker_statistics():
    data = spell_models.Statistic.get_all_as_dict()
    response = dict(content=data, status=200, message="OK")

    return jsonify(response)

@app.route("/api/bufftracker/modifiers/")
def buff_tracker_modifiers():
    data = spell_models.ModifierType.get_all_as_dict()
    response = dict(content=data, status=200, message="OK")

    return jsonify(response)