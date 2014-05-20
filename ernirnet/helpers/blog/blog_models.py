from ernirnet import db
from sqlalchemy import func
from datetime import date, datetime

role_user = 0
role_admin = 1

tag_association = db.Table("tag_assignments",
                           db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
                           db.Column("blog_id", db.Integer, db.ForeignKey("blog.id")),
                           info={"bind_key": "blog"})


class Blog(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    body = db.Column(db.Text())
    date = db.Column(db.Date())
    url = db.Column(db.Text(), unique=True)
    tags = db.relationship("Tag", secondary=tag_association, backref=db.backref("blogs", lazy="dynamic"))
    comments = db.relationship("Comment", backref="blog", order_by="Comment.date")

    def __init__(self, title, body, date):
        self.title = title
        self.url = Blog._url_from_title(title)
        self.body = body
        self.date = date

    @staticmethod
    def _url_from_title(title):
        url = title.replace(" ", "-")
        bad_symbols = "!*'();:@&=+$,./?%#[]"
        for symbol in bad_symbols:
            url = url.replace(symbol, "")
        url = url.lower()

        return url

    @classmethod
    def get_by_date(cls):
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def get_by_tag(cls, tag_name):
        all_blogs = cls.get_by_date()
        tag = Tag.query.filter_by(name=tag_name).first()

        blogs = []
        for blog in all_blogs:
            if tag in blog.tags:
                blogs.append(blog)

        return blogs

    @classmethod
    def get_by_url(cls, blog_url):
        # The intertron says it's "basically impossible" to inject SQLAlchemy. I'm going to trust that.
        blog = Blog.query.filter_by(url=blog_url).first()

        if blog is None:
            blog = cls.get_empty()

        return [blog]

    @classmethod
    def get_empty(cls):
        blog = cls("Oh no!",
                   "<p>The blog engine gremlins did not find any blogs matching your description. Try another?</p>",
                   date=date.today())
        blog.tags = [Tag("Whoops")]
        return blog


class Tag(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_usage(cls):
        return cls.query.with_entities(cls.name, func.count(cls.id).label("frequency")).join(tag_association).join(
            Blog).group_by(cls.id).order_by("frequency DESC").all()


class Comment(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    date = db.Column(db.Date())
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))

    def __init__(self, content, date):
        self.content = content
        self.date = date


    @classmethod
    def get_by_date(cls):
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def commit(cls, blog_id, text, user):
        blog = Blog.query.filter_by(id=blog_id).first()
        comment = cls(text, datetime.now())
        comment.author = user
        blog.comments.append(comment)

        db.session.commit()

    @classmethod
    def delete(cls, comment_id):
        comment = cls.query.filter_by(id=comment_id).first()
        db.session.delete(comment)
        db.session.commit()


class User(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.SmallInteger, default=role_user)
    comments = db.relationship("Comment", backref="author")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)