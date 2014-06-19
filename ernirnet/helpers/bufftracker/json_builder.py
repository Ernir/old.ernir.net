from ernirnet.helpers.bufftracker import spell_models

__author__ = 'ernir'


def build_json():
    spells = spell_models.Spell.query.all()
    spell_list = [spell.serialize() for spell in spells]

    modifier_types = spell_models.ModifierType.query.all()
    modifier_list = [modifier.serialize() for modifier in modifier_types]

    numerical_bonuses = spell_models.NumericalBonus.query.all()
    numerical_bonuses_list = [bonus.serialize() for bonus in numerical_bonuses]

    statistics = spell_models.Statistic.query.all()
    statistics_list = [statistic.serialize() for statistic in statistics]

    content = dict(spells=spell_list, modifierTypes=modifier_list, numericalBonuses=numerical_bonuses_list,
                   statistics=statistics_list)

    return dict(content=content, status=200, message="OK")