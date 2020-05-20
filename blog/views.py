from django.shortcuts import render, get_object_or_404

from blog.models import Entry, Comment, Tag
from blog.forms import CommentForm
from datetime import datetime


def index(request, language_filter=None):
    """

    The list of all blogs.
    """

    entries = Entry.visible_entries
    tags = Tag.objects_by_entry_count.all()

    if language_filter is not None:
        entries = entries.filter(language__iexact=language_filter)

    return render(request, "blog_list.html", {"entries": entries.all(), "tags": tags})


def entry(request, blog_slug):
    """

    Defines the page of a single blog entry.
    Finds the entry based on its slugified title, passed in by blog_slug.
    """

    the_entry = get_object_or_404(Entry, slug=blog_slug)
    tags = Tag.objects_by_entry_count.all()
    comment_form = CommentForm()

    if request.method == "POST":
        new_comment = Comment()
        new_comment.content = request.POST["content"]
        new_comment.author = request.user
        new_comment.published = datetime.now()
        new_comment.associated_with = the_entry
        new_comment.save()

    return render(
        request,
        "individual_blog.html",
        {"entry": the_entry, "comment_form": comment_form, "tags": tags},
    )


def by_tag(request, tag_slug):
    """

    A list of blogs with entries having a tag with the given tag_slug.
    """
    entries = Entry.visible_entries.filter(tags__slug=tag_slug).all()
    tags = Tag.objects_by_entry_count.all()

    return render(request, "blog_list.html", {"entries": entries, "tags": tags})
