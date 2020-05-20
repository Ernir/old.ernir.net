from django.shortcuts import render
from indexpage.models import Section


def main_index(request):
    """

    Ernir.net's main index page.
    """

    sections = Section.objects.all()

    return render(request, "main_index.html", {"sections": sections})
