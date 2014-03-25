from sqlalchemy import func
from ernirnet.blog_models import Tags, tag_association, Blogs
from datetime import date

def get_tags_ordered_by_usage():
    return Tags.query.with_entities(Tags.name, func.count(Tags.id).label("frequency")).join(tag_association).join(
        Blogs).group_by(Tags.id).order_by("frequency DESC").all()

def get_blogs_ordered_by_date():
    raw_blogs = Blogs.query.with_entities(Blogs.title,Blogs.body,Blogs.date,Tags.name).join(tag_association).join(Tags).order_by(Blogs.date.desc()).all()

    blogs = combine_entries(raw_blogs)

    return blogs

def get_blog_by_title(blog_title):
    # The intertron says it's "basically impossible" to inject SQLAlchemy. I'm going to trust that.
    raw_blogs = Blogs.query.with_entities(Blogs.title,Blogs.body,Blogs.date,Tags.name).filter_by(title = blog_title).join(tag_association).join(Tags).all()

    print("stuff")
    print(isinstance(raw_blogs,list))
    if len(raw_blogs) > 0:
        blog = combine_entries(raw_blogs)
    else:
        blog = get_empty_post()

    return blog

def combine_entries(raw_blogs):
    last_blog = dict(title=raw_blogs[0][0], body=raw_blogs[0][1], date=raw_blogs[0][2], tags=[raw_blogs[0][3]])
    blogs = [last_blog]
    if len(raw_blogs) > 1:
        for raw_blog in raw_blogs[1:]:
            if last_blog["title"] == raw_blog[0]:
                blogs[-1]["tags"].append(raw_blog[3])
            else:
                last_blog = dict(title=raw_blog[0], body=raw_blog[1], date=raw_blog[2], tags=[raw_blog[3]])
                blogs.append(last_blog)
    return blogs

def get_empty_post():
    return [dict(title="Oh no!", body = "<p>The blog engine gremlins did not find any blogs matching your description. Try another?</p>",date=date.today(),tags=["Whoops"])]