__author__ = 'ernir'

from ernirnet import db


class Spells(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Spell %r>" % self.name

    def serialize(self):
        return dict(id=self.id, name=self.name)


class ModifierTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<ModifierType %r>" % self.name

    def serialize(self):
        return dict(id=self.id, name=self.name)


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Statistic %r>" % self.name

    def serialize(self):
        return dict(id=self.id, name=self.name)


class NumericalBonuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bonus = db.Column(db.String(120))
    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spells.id"))
    associated_spell = db.relationship("Spells", backref=db.backref("numerical_benefits", lazy="dynamic"))
    modifier_type_id = db.Column(db.Integer, db.ForeignKey("modifier_types.id"))
    modifier_type = db.relationship("ModifierTypes")
    applicable_to_id = db.Column(db.Integer, db.ForeignKey("statistics.id"))
    applicable_to = db.relationship("Statistics")

    def __init__(self, spell, bonus, type, applies_to):
        self.bonus = bonus
        self.associated_spell = spell
        self.modifier_type = type
        self.applicable_to = applies_to

    def __repr__(self):
        return "<Numerical spell bonus described by the function %r>" % self.bonus

    def serialize(self):
        return dict(id=self.id, bonus=self.bonus, associatedSpell=self.associated_spell_id,
                    modifier=self.modifier_type_id, applicableTo=self.applicable_to_id)


class MiscBonuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bonus_description = db.Column(db.String(120))
    associated_spell_id = db.Column(db.Integer, db.ForeignKey("spells.id"))
    associated_spell = db.relationship("Spells", backref=db.backref("misc_benefits", lazy="dynamic"))

    def __init__(self, spell, description):
        self.bonus_description = description
        self.associated_spell = spell

    def __repr__(self):
        return "<Misc Bonus %r>" % self.bonus_description