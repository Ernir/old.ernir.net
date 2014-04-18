from ernirnet import db

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


class Tag(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)

    def __init__(self, name):
        self.name = name


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