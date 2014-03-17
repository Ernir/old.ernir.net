'''
This is a database definition helper file. Run to generate spells.db.
'''

from ernirnet import db
from ernirnet.spell_models import Spells, ModifierTypes, NumericalBonuses, MiscBonuses, Statistics

db.drop_all()
db.create_all()

spell_list = ["Aid", "Barkskin", "Bear's Endurance", "Bless", "Blink", "Blur", "Bull's Strength", "Cat's Grace"]
spells = dict()

for spell in spell_list:
    spells[spell] = Spells(spell)
    db.session.add(spells[spell])

modifier_type_list = ["alchemical", "armor", "circumstance", "competence", "deflection", "dodge", "enhancement",
                      "insight", "luck", "morale", "natural armor", "profane", "racial", "resistance", "sacred",
                      "shield", "size", "untyped"]
modifiers = dict()

for type in modifier_type_list:
    modifiers[type] = ModifierTypes(type)
    db.session.add(modifiers[type])

statistics_list = ["attack", "constitution", "fear", "strength", "natural armor", "tempHP"]
statistics = dict()

for stat in statistics_list:
    statistics[stat] = Statistics(stat)
    db.session.add(statistics[stat])

db.session.add(NumericalBonuses(spells["Aid"], "+1", modifiers["morale"], statistics["attack"]))
db.session.add(NumericalBonuses(spells["Aid"], "+1", modifiers["morale"], statistics["fear"]))
# db.session.add(MiscBonuses(spells["Aid"], "1d8+CL Temp HP, max 1d8+10"))
db.session.add(
    NumericalBonuses(spells["Aid"], "_1d8plusCL_Max1d8plus10(CL)", modifiers["untyped"], statistics["tempHP"]))
db.session.add(NumericalBonuses(spells["Barkskin"], "_2plus1per3CL_Max5(CL)", modifiers["enhancement"],
                                statistics["natural armor"]))
db.session.add(NumericalBonuses(spells["Bear's Endurance"], "+4", modifiers["enhancement"], statistics["constitution"]))
db.session.add(NumericalBonuses(spells["Bless"], "+1", modifiers["morale"], statistics["attack"]))
db.session.add(NumericalBonuses(spells["Bless"], "+1", modifiers["morale"], statistics["fear"]))
db.session.add(NumericalBonuses(spells["Bull's Strength"], "+4", modifiers["enhancement"], statistics["strength"]))

db.session.commit()
