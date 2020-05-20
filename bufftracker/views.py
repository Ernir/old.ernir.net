from bufftracker.calculations import get_applicable_bonuses, get_misc_bonuses
from bufftracker.models import Spell, Source, StatisticGroup
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    spell_list = Spell.objects.all()
    source_list = Source.objects.all()

    return render(
        request, "index.html", {"spell_list": spell_list, "source_list": source_list}
    )


def get_statistics(request):

    groups_query = StatisticGroup.objects
    groups = [group.get_as_dict() for group in groups_query.all()]

    return JsonResponse({"groups": groups})


def calculate_bonuses(request):
    if request.method == "GET":
        raw_cl_dict = request.GET

        cl_dict = {}
        for key, val in raw_cl_dict.dict().items():
            cl_dict[int(key)] = int(val)

        numerical_bonuses = get_applicable_bonuses(cl_dict)
        misc_bonuses = get_misc_bonuses(cl_dict)

        content = {"numerical": numerical_bonuses, "misc": misc_bonuses}

        return JsonResponse({"content": content,})
