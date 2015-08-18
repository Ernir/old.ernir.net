from django.shortcuts import render


def main_index(request):
    """

    Ernir.net's main index page.
    """

    return render(request, "main_index.html", {})