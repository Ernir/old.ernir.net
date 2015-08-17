from django.shortcuts import render, get_object_or_404

from blog.models import Entry, Comment
from blog.forms import CommentForm
from datetime import datetime


def index(request):
    """

    The list of all blogs.
    """

    entries = Entry.objects.all()

    return render(request, "blog_list.html", {"entries": entries})


def entry(request, blog_slug):
    """

    Defines the page of a single blog entry.
    Finds the entry based on its slugified title, passed in by blog_slug.
    """

    the_entry = get_object_or_404(Entry, slug=blog_slug)
    comment_form = CommentForm()

    if request.method == "POST":
        new_comment = Comment()
        new_comment.content = request.POST["content"]
        new_comment.author = request.user
        new_comment.published = datetime.now()
        new_comment.associated_with = the_entry
        new_comment.save()

    return render(request, "individual_blog.html", {
        "entry": the_entry,
        "comment_form": comment_form
    })