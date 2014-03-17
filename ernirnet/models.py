__author__ = 'ernir'

from ernirnet import db


class Spells(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Spell %r>" % self.name


class ModifierTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<ModifierType %r>" % self.name


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Statistic %r>" % self.name


class NumericalBonuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bonus = db.Column(db.String(120))
    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spells.id"))
    associated_spell = db.relationship("Spells", backref=db.backref("bonuses", lazy="dynamic"))
    modifier_type_id = db.Column(db.Integer, db.ForeignKey("modifier_types.id"))
    modifier_type = db.relationship("ModifierTypes")
    applicable_to_id = db.Column(db.Integer, db.ForeignKey("statistics.id"))
    applicable_to = db.relationship("Statistics")

    def __init__(self, bonus, spell, type, applies_to):
        self.bonus = bonus
        self.associated_spell = spell
        self.modifier_type = type
        self.applicable_to = applies_to


    def __repr__(self):
        pass #TODO