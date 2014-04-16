from datetime import date

from sqlalchemy import func

from ernirnet.helpers.blog.blog_models import Tag, tag_association, Blog
from ernirnet import db


def get_tags_ordered_by_usage():
    return Tag.query.with_entities(Tag.name, func.count(Tag.id).label("frequency")).join(tag_association).join(
        Blog).group_by(Tag.id).order_by("frequency DESC").all()


def create_tag_if_new(proposed_name):
    if Tag.query.filter_by(name=proposed_name).count() == 0:
        db.session.add(Tag(proposed_name))


def get_blogs_ordered_by_date():
    raw_blogs = Blog.query.with_entities(Blog.title, Blog.body, Blog.date, Blog.url, Tag.name).join(
        tag_association).join(Tag).order_by(Blog.date.desc()).all()

    blogs = combine_entries(raw_blogs)

    return blogs


def get_blogs_by_tag(tag_name):
    all_blogs = get_blogs_ordered_by_date()

    blogs = []
    for blog in all_blogs:
        if tag_name in blog["tags"]:
            blogs.append(blog)

    return blogs


def get_blog_by_title(blog_url):
    # The intertron says it's "basically impossible" to inject SQLAlchemy. I'm going to trust that.
    raw_blogs = Blog.query.with_entities(Blog.title, Blog.body, Blog.date, Blog.url, Tag.name).filter_by(
        url=blog_url).join(tag_association).join(Tag).all()

    if len(raw_blogs) > 0:
        blog = combine_entries(raw_blogs)
    else:
        blog = get_empty_post()

    return blog


def combine_entries(raw_blogs):
    last_blog = dict(title=raw_blogs[0][0], body=raw_blogs[0][1], date=raw_blogs[0][2], url=raw_blogs[0][3],
                     tags=[raw_blogs[0][4]])
    blogs = [last_blog]
    if len(raw_blogs) > 1:
        for raw_blog in raw_blogs[1:]:
            if last_blog["title"] == raw_blog[0]:
                blogs[-1]["tags"].append(raw_blog[4])
            else:
                last_blog = dict(title=raw_blog[0], body=raw_blog[1], date=raw_blog[2], url=raw_blog[3],
                                 tags=[raw_blog[4]])
                blogs.append(last_blog)
    return blogs


def get_empty_post():
    return [dict(title="Oh no!",
                 body="<p>The blog engine gremlins did not find any blogs matching your description. Try another?</p>",
                 url="error", date=date.today(), tags=["Whoops"])]