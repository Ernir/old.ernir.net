from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vanciantopsionics.models import VtPFile, Chapter


def vtp_index(request):
    """

    The index page for the VtP project description.
    """

    vtp_files = VtPFile.objects.all()

    latest_file = vtp_files[0]
    older_files = vtp_files[1:]

    all_chapters = Chapter.objects.values("title", "order")

    category = "index"

    return render(request, "vtp_main.html", {
        "latest_file": latest_file,
        "older_files": older_files,
        "chapters": all_chapters,
        "category": category
    })


def vtp_chapter(request, chapter_number):
    chapter = get_object_or_404(Chapter, order=chapter_number)
    all_chapters = Chapter.objects.values("title", "order")
    category = "chapter"

    return render(request, "single_chapter.html", {
        "chapter": chapter,
        "chapters": all_chapters,
        "category": category
    })