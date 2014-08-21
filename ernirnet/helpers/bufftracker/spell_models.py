__author__ = 'ernir'

from ernirnet import db
from sqlalchemy import func


class Spell(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    source = db.Column(db.String(3), default="SRD")
    real_spell = db.Column(db.Boolean, default=True)
    variable = db.Column(db.Boolean, default=False)

    def __init__(self):
        pass

    def __init__(self, name=None, source="SRD", real_spell=True, variable=False):
        self.name = name
        self.source = source
        self.real_spell = real_spell
        self.variable = variable

    @classmethod
    def get_all_as_list(cls):
        all_spells = cls.query.order_by(cls.name).all()

        return_list = [dict(id=spell.id,
                            name=spell.name,
                            source=spell.source,
                            variable=spell.variable) for spell in all_spells]

        return return_list

    def __str__(self):
        return str.format("<{}>", self.name)

    def __repr__(self):
        return self.__str__()


class ModifierType(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self):
        pass

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_all_as_dict(cls):
        all_modifiers = cls.query.all()

        return_dict = dict()
        for modifier in all_modifiers:
            return_dict[modifier.id] = modifier.name

        return return_dict

    def __str__(self):
        return str.format("<{}>", self.name)

    def __repr__(self):
        return self.__str__()


class Statistic(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self):
        pass

    def __init__(self, name="No Name"):
        self.name = name

    @classmethod
    def get_all_as_dict(cls):
        all_statistics = cls.query.all()

        return_dict = dict()
        for stat in all_statistics:
            return_dict[stat.id] = stat.name

        return return_dict

    def __str__(self):
        return str.format("<{}>", self.name)

    def __repr__(self):
        return self.__str__()


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

    def __init__(self):
        pass

    def __init__(self,
                 spell=None,
                 bonus=None,
                 applicable_range=[float("-inf"), float("inf")],
                 modifier_type=None,
                 applies_to=None):

        if len(applicable_range) == 2 and applicable_range[1] >= applicable_range[0]:
            self.min_level = applicable_range[0]
            self.max_level = applicable_range[1]

        self.bonus = bonus
        self.associated_spell = spell
        self.modifier_type = modifier_type
        self.applicable_to = applies_to

    def __str__(self):
        return str.format("<Applies {0} {1} bonus to {2} at levels {3} to {4}>",
                          self.bonus,
                          self.modifier_type.name,
                          self.applicable_to.name,
                          self.min_level,
                          self.max_level)

    def __repr__(self):
        return str.format("<NumericalBonus {0}>", self.id)

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

    @classmethod
    def get_applicable_as_dict_detailed(cls, cl_dictionary):

        result = {}

        selected_spell_ids = [key for key in cl_dictionary]

        statistics = Statistic.query.with_entities(Statistic.id, Statistic.name).all()

        for statistic in statistics:

            bonuses = NumericalBonus.query.filter(False)
            for spell_id in selected_spell_ids:
                in_range = NumericalBonus.query.filter(cls.min_level <= cl_dictionary[spell_id],
                                                       cls.max_level >= cl_dictionary[spell_id],
                                                       cls.applicable_to_id == statistic.id,
                                                       cls.associated_spell_id == spell_id)
                bonuses = bonuses.union(in_range)

            collapsed = bonuses.group_by(cls.modifier_type_id).with_entities(func.max(cls.bonus).label("highest"))

            result[statistic.id] = db.session.query(func.sum(collapsed.subquery().columns.highest)).scalar()

        return result


class MiscBonus(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    bonus_description = db.Column(db.String(120))
    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spell.id"))
    associated_spell = db.relationship("Spell", backref=db.backref("misc_benefits", lazy="dynamic"))

    @classmethod
    def get_applicable_as_list(cls, spell_ids):

        result = []

        columns = Spell.query.with_entities(Spell.id, MiscBonus.bonus_description)
        selected_spells = columns.filter(Spell.id.in_(spell_ids)).join(MiscBonus)
        all_bonuses = selected_spells.join(MiscBonus)
        unique_bonuses = all_bonuses.group_by(MiscBonus.bonus_description).all()

        for bonus in unique_bonuses:
            result.append(bonus[1])

        return result

    def __init__(self):
        pass

    def __init__(self, spell=None, description=None):
        self.bonus_description = description
        self.associated_spell = spell

    def __str__(self):
        return str.format("<{}>", self.bonus_description)

    def __repr__(self):
        return str.format("<MiscBonus object {0}. Effect: {1}>", self.id, self.bonus_description)