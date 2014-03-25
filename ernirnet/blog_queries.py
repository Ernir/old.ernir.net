from sqlalchemy import func
from ernirnet.blog_models import Tags, tag_association, Blogs


def get_tags_ordered_by_usage():
    return Tags.query.with_entities(Tags.name, func.count(Tags.id).label("frequency")).join(tag_association).join(
        Blogs).group_by(Tags.id).order_by("frequency DESC").all()

def get_blogs_ordered_by_date():
    raw_blogs = Blogs.query.with_entities(Blogs.title,Blogs.body,Blogs.date,Tags.name).join(tag_association).join(Tags).order_by(Blogs.date.desc()).all()

    last_blog = dict(title = raw_blogs[0][0], body=raw_blogs[0][1], date=raw_blogs[0][2], tags=[raw_blogs[0][3]])
    blogs = [last_blog]
    if len(raw_blogs) > 1:
        for raw_blog in raw_blogs[1:]:
            if last_blog["title"] == raw_blog[0]:
                blogs[-1]["tags"].append(raw_blog[3])
            else:
                last_blog = dict(title=raw_blog[0],body=raw_blog[1],date=raw_blog[2],tags=[raw_blog[3]])
                blogs.append(last_blog)

    return blogs


# posts = [dict(title="First title", date=date(2014, 3, 24), body="First body", tags=["Tag1"]),
#              dict(title="Second title", date=date(2014, 3, 24), body="Second body", tags=["Tag1", "Tag2", "Tag3"])]