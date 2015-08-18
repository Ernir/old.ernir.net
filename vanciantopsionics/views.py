from django.shortcuts import render
from vanciantopsionics.models import VtPFile


def vtp_index(request):
    """

    The index page for the VtP project description.
    """

    vtp_files = VtPFile.objects.all()

    latest_file = vtp_files[0]
    older_files = vtp_files[1:]

    return render(request, "vtp_main.html", {
        "latest_file": latest_file,
        "older_files": older_files
    })