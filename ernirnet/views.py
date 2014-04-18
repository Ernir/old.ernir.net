from flask import render_template, jsonify, request, flash, redirect, g, url_for, session
from flask_login import login_user, logout_user, current_user, login_required

from ernirnet import app, lm, oid, db
from ernirnet.helpers.blog import blog_statements
from ernirnet.helpers.blog.blog_models import role_user
from ernirnet.helpers.blog.blog_models import User
from ernirnet.helpers.blog.forms import LoginForm
from ernirnet.helpers.bufftracker import spell_models
from ernirnet.helpers.bufftracker.json_builder import build_json
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
    posts = blog_statements.get_blogs_ordered_by_date()
    tags = blog_statements.get_tags_ordered_by_usage()

    return render_template("blog.jinja2", sitename=u"Blog", posts=posts, tags=tags)


@app.route("/blog/<blog_url>/")
def individual_blog(blog_url):
    blog = blog_statements.get_blog_by_title(blog_url)
    tags = blog_statements.get_tags_ordered_by_usage()

    return render_template("blog.jinja2", sitename=u"Blog", posts=blog, tags=tags)


@app.route("/blog/tags/<tag_name>/")
def tagged_blogs(tag_name):
    blogs = blog_statements.get_blogs_by_tag(tag_name)
    tags = blog_statements.get_tags_ordered_by_usage()

    return render_template("blog.jinja2", sitename=u"Blog", posts=blogs, tags=tags)


'''
Admin and login
'''


@app.route("/admin/")
@login_required
def admin():
    if g.user.role == 1:
        return render_template("admin.jinja2", sitename=u"Admin")
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
    spell_objects = spell_models.Spells.query.order_by(spell_models.Spells.id).all()
    spell_list = [spell.serialize() for spell in spell_objects]

    return render_template("bufftracker.jinja2", spell_list=spell_list, sitename=u"D&D 3.5 Buff Tracker")


'''
API routes
'''


@app.route("/api/parseMW")
def mw_parse_api():
    sheet_id = request.args.get("id", 0, type=int)

    try:
        data = Parser().get_mw_data(sheet_id)
    except:
        raise InvalidUsage("No Myth-Weavers sheet with the given ID was found", status_code=400)
    return jsonify(data)


@app.route("/api/bufftracker")
def buff_tracker_api():
    json_dict = build_json()
    return jsonify(json_dict)
