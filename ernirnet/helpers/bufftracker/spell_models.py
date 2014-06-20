from reportlab.graphics.charts.piecharts import theta0

__author__ = 'ernir'

from ernirnet import db
from sqlalchemy import func


class Spell(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    source = db.Column(db.String(3))
    real_spell = db.Column(db.Boolean)

    def __init__(self, name, source="SRD", real_spell=True):
        self.name = name
        self.source = source
        self.real_spell = real_spell

    @classmethod
    def get_all_as_list(cls):
        all_spells = cls.query.order_by(cls.name).all()

        return_list = [dict(id=spell.id, name=spell.name, source=spell.source) for spell in all_spells]

        return return_list


class ModifierType(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_all_as_dict(cls):
        all_modifiers = cls.query.all()

        return_dict = dict()
        for modifier in all_modifiers:
            return_dict[modifier.id] = modifier.name

        return return_dict


class Statistic(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_all_as_dict(cls):
        all_statistics = cls.query.all()

        return_dict = dict()
        for stat in all_statistics:
            return_dict[stat.id] = stat.name

        return return_dict


class NumericalBonus(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    bonus = db.Column(db.Integer)
    min_level = db.Column(db.Float)
    max_level = db.Column(db.Float)

    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spell.id"))
    associated_spell = db.relationship("Spell", backref=db.backref("numerical_benefits", lazy="dynamic"))
    modifier_type_id = db.Column(db.Integer, db.ForeignKey("modifier_type.id"))
    modifier_type = db.relationship("ModifierType")
    applicable_to_id = db.Column(db.Integer, db.ForeignKey("statistic.id"))
    applicable_to = db.relationship("Statistic")

    def __init__(self, spell, bonus, applicable_range, modifier_type, applies_to):

        if len(applicable_range) == 2 and applicable_range[1] >= applicable_range[0]:
            self.min_level = applicable_range[0]
            self.max_level = applicable_range[1]

        self.bonus = bonus
        self.associated_spell = spell
        self.modifier_type = modifier_type
        self.applicable_to = applies_to

    @classmethod
    def get_applicable_as_dict(cls, level, spell_ids):

        result = dict()

        statistics = Statistic.query.with_entities(Statistic.id, Statistic.name).all()

        for statistic in statistics:
            columns = Spell.query.join(cls).with_entities(func.max(cls.bonus).label("highest"))
            selected_spells = columns.filter(Spell.id.in_(spell_ids))
            bonuses_in_range = selected_spells.filter(cls.min_level <= level, cls.max_level >= level)
            applicable_to_current_statistic = bonuses_in_range.filter(cls.applicable_to_id == statistic.id)
            collapsed_by_modifier = applicable_to_current_statistic.group_by(cls.modifier_type_id)

            result[statistic.id] = db.session.query(func.sum(collapsed_by_modifier.subquery().columns.highest)).scalar()

        return result


class MiscBonus(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    bonus_description = db.Column(db.String(120))
    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spell.id"))
    associated_spell = db.relationship("Spell", backref=db.backref("misc_benefits", lazy="dynamic"))

    def __init__(self, spell, description):
        self.bonus_description = description
        self.associated_spell = spell