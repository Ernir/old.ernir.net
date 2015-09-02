from bufftracker.models import Statistic, NumericalBonus, MiscBonus, TempHPBonus


def get_applicable_bonuses(cl_dict):
    """

    Calculates the total bonuses given by all selected spells, accounting for
    stacking rules.

    :param cl_dict: A dictionary with selected spell IDs as keys,
    and the CLs of each spell as values.
    :return: A dictionary with statistic IDs as keys,
    and the calculated bonuses as values.
    """
    result = {}

    selected_spell_ids = [key for key in cl_dict]

    statistics = Statistic.objects.all()

    for statistic in statistics:
        # Getting those bonuses that actually apply to the current stat
        applicable = NumericalBonus.objects.filter(applies_to=statistic)

        # The results must be broken down by modifier types.
        mod_type_dict = {}

        for bonus in applicable.all():
            for spell in bonus.spell_set.all():
                if spell.id in selected_spell_ids:
                    formula = bonus.bonus_formula
                    if formula:
                        value = formula.calculate(cl_dict[spell.id])
                        type_id = bonus.modifier_type.id
                        if type_id in mod_type_dict:
                            mod_type_dict[type_id] = max(
                                mod_type_dict[type_id], value
                            )
                        else:
                            mod_type_dict[type_id] = value

        result[statistic.id] = sum(mod_type_dict.values())

    return result


def get_temp_hp_bonuses(cl_dict):

    selected_spell_ids = [key for key in cl_dict]

    bonuses = TempHPBonus.objects.filter(spell__in=selected_spell_ids)


# class TempHPBonus(models.Model):
#     die_number_formula = models.ForeignKey(
#         CasterLevelFormula,
#         related_name="die_number",
#         null=True
#     )
#     die_size = models.IntegerField(default=0)
#     other_bonus_formula = models.ForeignKey(
#         CasterLevelFormula,
#         related_name="other_bonus",
#         null=True
#     )

def get_misc_bonuses(cl_dict):
    """

    Lists the total non-numerical bonuses given by all selected spells.

    :param cl_dict: A dictionary with selected spell IDs as keys,
    and the CLs of each spell as values.
    :return: A list of the descriptions of the spells' non-numerical bonuses.

    """

    result = set()  # Set guarantees uniqueness.

    selected_spell_ids = [key for key in cl_dict]

    bonuses = MiscBonus.objects.filter(spell__in=selected_spell_ids)

    for bonus in bonuses.all():
        result.add(bonus.description)

    return list(result)