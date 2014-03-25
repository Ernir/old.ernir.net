__author__ = 'ernir'

from ernirnet import db

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
        self.url = title.replace(" ", "-").lower()
        self.body = body
        self.date = date


class Tags(db.Model):
    __bind_key__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)

    def __init__(self, name):
        self.name = name