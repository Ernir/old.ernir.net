from django.shortcuts import render

from blog.models import Entry


def index(request):
    """

    The main page.
    """

    blogs = Entry.objects.all()

    return render(request, "index.html", {"blogs": blogs})