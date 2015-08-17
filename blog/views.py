from django.shortcuts import render, get_object_or_404

from blog.models import Entry


def index(request):
    """

    The main page.
    """

    entries = Entry.objects.all()

    return render(request, "blog_list.html", {"entries": entries})


def entry(request, blog_slug):
    """

    Defines the page of a single maneuver.
    Finds the maneuver based on its slugified name, passed in by man_slug.
    """

    the_entry = get_object_or_404(Entry, slug=blog_slug)

    return render(request, "individual_blog.html", {"entry": the_entry})