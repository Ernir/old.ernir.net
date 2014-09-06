__author__ = 'ernir'

from ernirnet import db
from sqlalchemy import func


class Source(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(4))  # Example values: "SRD", "SPC"
    name = db.Column(db.String(80))  # Example values: "d20 SRD", "Spell Compendium"
    priority = db.Column(db.Integer)  # Sources with a lower priority number are printed first.

    def __init__(self, name=None, short=None, priority=100):
        self.name = name
        self.short = short
        self.priority = priority

    @classmethod
    def get_all(cls):
        all_sources = cls.query.with_entities(cls.id, cls.short, cls.name).order_by(cls.priority).all()

        return all_sources

    def __str__(self):
        return str.format("<{}>", self.short)

    def __repr__(self):
        return self.__str__()


class Spell(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))  # Example values: "Aid", "Barkskin"
    source_id = db.Column(db.Integer, db.ForeignKey("source.id"))
    source = db.relationship("Source")
    real_spell = db.Column(db.Boolean, default=True)  # Bonuses resulting from magic items also appear in this table.
    variable = db.Column(db.Boolean, default=False)  # A spell that varies by CL needs special UI elements.
    size_modifying = db.Column(db.Boolean, default=False)  # Size-modifying spells can not stack.

    def __init__(self, name=None, source=None, variable=False, real_spell=True, size_modifying=False):
        self.name = name
        self.source = source
        self.variable = variable
        self.real_spell = real_spell
        self.size_modifying = size_modifying

    @classmethod
    def get_all(cls):
        all_spells = cls.query.with_entities(cls.id,
                                             cls.name,
                                             cls.source_id,
                                             cls.variable,
                                             cls.size_modifying).order_by(cls.name).all()

        return all_spells

    def __str__(self):
        return str.format("<{}>", self.name)

    def __repr__(self):
        return self.__str__()


class ModifierType(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))  # Example values: "deflection", "dodge", "enhancement"...

    def __init__(self, name=None):
        self.name = name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_as_dict(cls):
        all_modifiers = cls.get_all()

        return_dict = {}
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
    name = db.Column(db.String(80))  # Example values: "Attack bonus", "Damage", "Saves vs. fear"
    group_id = db.Column(db.Integer, db.ForeignKey("statistics_group.id"))
    group = db.relationship("StatisticsGroup")

    def __init__(self, name=None, group=None):
        self.name = name
        self.group = group

    @classmethod
    def get_all_as_dict(cls):
        all_stat_groups = StatisticsGroup.get_all()

        return_dict = {}

        for group in all_stat_groups:
            associated_statistics = cls.query.filter(cls.group_id == group.id)
            group_dict = {}
            for stat in associated_statistics:
                group_dict[stat.id] = stat.name
            return_dict[group.priority] = group_dict

        return return_dict

    def __str__(self):
        return str.format("<{}>", self.name)

    def __repr__(self):
        return self.__str__()


class StatisticsGroup(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))  # Example values: "Ability Scores", "Saves"
    priority = db.Column(db.Integer)  # Groups with lower priority are printed first

    def __init__(self, name=None, priority=0):
        self.name = name
        self.priority = priority

    @classmethod
    def get_all(cls):
        return cls.query.order_by(StatisticsGroup.priority).all()

    def __str__(self):
        return str.format("<{}>", self.name)

    def __repr__(self):
        return self.__str__()


class NumericalBonus(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    bonus = db.Column(db.Integer)
    min_level = db.Column(db.Float)  # Each NumericalBonus entry applies in a fixed level range. Multiple entries
    max_level = db.Column(db.Float)  # are needed to represent values that vary by level.

    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spell.id"))
    associated_spell = db.relationship("Spell", backref=db.backref("numerical_benefits", lazy="dynamic"))
    modifier_type_id = db.Column(db.Integer, db.ForeignKey("modifier_type.id"))
    modifier_type = db.relationship("ModifierType")
    applicable_to_id = db.Column(db.Integer, db.ForeignKey("statistic.id"))
    applicable_to = db.relationship("Statistic")

    def __init__(self,
                 spell=None,
                 bonus=None,
                 applicable_range=(float("-inf"), float("inf")),
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
    def get_applicable_as_dict(cls, cl_dictionary):
        """ Calculates the total bonuses given by all selected spells, accounting for stacking rules.

        cl_dictionary: A dictionary with spell IDs as keys, and the CLs of each spell as values.

        returns: A dictionary with statistic IDs as keys, and the calculated bonuses as values."""

        result = {}

        selected_spell_ids = [key for key in cl_dictionary]

        statistics = Statistic.query.with_entities(Statistic.id, Statistic.name).all()

        for statistic in statistics:

            # We start with an empty query
            bonuses = NumericalBonus.query.filter(False)
            for spell_id in selected_spell_ids:
                # Iterate over spells, adding associated bonuses whose CLs matches the cl_dictionary value.
                in_range = NumericalBonus.query.filter(cls.min_level <= cl_dictionary[spell_id],
                                                       cls.max_level >= cl_dictionary[spell_id],
                                                       cls.applicable_to_id == statistic.id,
                                                       cls.associated_spell_id == spell_id)
                bonuses = bonuses.union(in_range)

            # Grouping and calculating.
            collapsed = bonuses.group_by(cls.modifier_type_id).with_entities(func.max(cls.bonus).label("highest"))
            result[statistic.id] = db.session.query(func.sum(collapsed.subquery().columns.highest)).scalar()

        return result


class MiscBonus(db.Model):
    __bind_key__ = "spells"

    id = db.Column(db.Integer, primary_key=True)
    bonus_description = db.Column(db.String(120))
    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spell.id"))
    associated_spell = db.relationship("Spell", backref=db.backref("misc_benefits", lazy="dynamic"))
    is_temp_hp_bonus = db.Column(db.Boolean)

    def __init__(self, spell=None, description=None, is_temp_hp_bonus=False):
        self.bonus_description = description
        self.associated_spell = spell
        self.is_temp_hp_bonus = is_temp_hp_bonus

    @classmethod
    def get_applicable_as_list(cls, spell_ids):

        result = []

        # Returns all distinct Misc. bonuses associated with spells of the given ids.
        # Temp HP bonus duplication allowed.
        columns = Spell.query.with_entities(Spell.id, MiscBonus.bonus_description)
        selected_spells = columns.filter(Spell.id.in_(spell_ids)).join(MiscBonus)

        exclude_temp_hp = selected_spells.filter(cls.is_temp_hp_bonus == False)  # PEP8 comparison no work? TODO: check
        include_temp_hp = selected_spells.filter(cls.is_temp_hp_bonus)

        unique_bonuses = exclude_temp_hp.group_by(MiscBonus.bonus_description).all()
        temp_hp_bonuses = include_temp_hp.all()

        for bonus in unique_bonuses:
            result.append(bonus[1])

        for temp_hp_bonus in temp_hp_bonuses:
            result.append(temp_hp_bonus[1])

        return result

    def __str__(self):
        return str.format("<{}>", self.bonus_description)

    def __repr__(self):
        return str.format("<MiscBonus object {0}. Effect: {1}>", self.id, self.bonus_description)