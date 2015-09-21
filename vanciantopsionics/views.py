import string
from collections import OrderedDict
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vanciantopsionics.models import VtPFile, Chapter, Spell


def vtp_index(request):
    """

    The index page for the VtP project description.
    """

    vtp_files = VtPFile.objects.all()

    latest_file = vtp_files[0]
    older_files = vtp_files[1:]

    all_chapters = Chapter.objects.values("title", "order")

    category = "home"

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


def vtp_spell(request, spell_slug):
    spell = get_object_or_404(Spell, slug=spell_slug)
    all_chapters = Chapter.objects.values("title", "order")
    category = "spell"

    return render(request, "single_spell.html", {
        "spell": spell,
        "chapters": all_chapters,
        "category": category
    })


def vtp_spell_index(request):

    category = "index"
    all_chapters = Chapter.objects.values("title", "order")

    alphabet = string.ascii_uppercase
    spell_bag = OrderedDict()
    # The letters where we break the columns.
    # This could be calculated with a fancy algorithm, but that's overkill.
    breaks = ["F", "Q"]

    spells = Spell.objects
    for letter in alphabet:
        spells_starting_with_letter = \
            spells.filter(title__startswith=letter).all()
        spell_bag[letter] = spells_starting_with_letter

    return render(request, "spell_index.html", {
        "category": category,
        "chapters": all_chapters,
        "spells_alphabetical": spell_bag,
        "breaks": breaks
    })