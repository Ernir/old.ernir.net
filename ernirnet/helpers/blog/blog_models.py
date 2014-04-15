from ernirnet import db

role_user = 0
role_admin = 1

tag_association = db.Table("tag_assignments",
                           db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
                           db.Column("blog_id", db.Integer, db.ForeignKey("blogs.id")),
                           info={"bind_key": "blog"})


class Blogs(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    body = db.Column(db.Text())
    date = db.Column(db.Date())
    url = db.Column(db.Text(), unique=True)
    tags = db.relationship("Tags", secondary=tag_association, backref=db.backref("blogs", lazy="dynamic"))

    def __init__(self, title, body, date):
        self.title = title
        self.url = self._url_from_title(title)
        self.body = body
        self.date = date

    def _url_from_title(self, title):
        url = title.replace(" ", "-")
        bad_symbols = "!*'();:@&=+$,./?%#[]"
        for symbol in bad_symbols:
            url = url.replace(symbol, "")
        url = url.lower()

        return url


class Tags(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)

    def __init__(self, name):
        self.name = name


class User(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.SmallInteger, default=role_user)
    # posts = db.relationship('Post', backref='author', lazy='dynamic') #TODO add references

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