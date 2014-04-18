from datetime import date

from sqlalchemy import func

from ernirnet.helpers.blog.blog_models import Tag, tag_association, Blog
from ernirnet import db

'''
General queries
'''


def get_tags_ordered_by_usage():
    return Tag.query.with_entities(Tag.name, func.count(Tag.id).label("frequency")).join(tag_association).join(
        Blog).group_by(Tag.id).order_by("frequency DESC").all()


def get_blogs_ordered_by_date():
    return Blog.query.order_by(Blog.date.desc()).all()


def get_blogs_by_tag(tag_name):
    all_blogs = get_blogs_ordered_by_date()
    tag = Tag.query.filter_by(name=tag_name).first()

    blogs = []
    for blog in all_blogs:
        if tag in blog.tags:
            blogs.append(blog)

    return blogs


def get_blog_by_title(blog_url):
    # The intertron says it's "basically impossible" to inject SQLAlchemy. I'm going to trust that.
    blog = Blog.query.filter_by(url=blog_url).first()

    if blog is None:
        blog = get_empty_post()

    return [blog]


'''
Insertion statements
'''


def create_tag_if_new(proposed_name):
    if Tag.query.filter_by(name=proposed_name).count() == 0:
        db.session.add(Tag(proposed_name))


'''
Helpers
'''

def get_empty_post():
    blog = Blog("Oh no!",
                "<p>The blog engine gremlins did not find any blogs matching your description. Try another?</p>",
                date=date.today())
    blog.tags = [Tag("Whoops")]
    return blog