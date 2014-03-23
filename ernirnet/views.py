from flask import render_template, jsonify, request, url_for
from os import listdir
from ernirnet.xml_parse import Parser
from ernirnet import app
from ernirnet.errors import InvalidUsage
import spell_models

'''
Main pages
'''

@app.route("/")
def heim():
    return render_template("index.jinja2", sitename=u"Home")

@app.route("/CV/") # Icelandic CV
def cv():
    return render_template("cv.jinja2", sitename=u"CV")

@app.route("/ferilskra/") # Icelandic CV
def ferilskra():
    return render_template("ferilskra.jinja2", sitename=u"CV")


@app.route("/contact/")
def contact():
    return render_template("contact.jinja2", sitename=u"Contact")


'''
Hobby subpages
'''

@app.route("/vanciantopsionics/")
def vtp():

    # TODO: Generate this
    version_numbers = reversed(
        ["103", "104", "105", "105a", "106", "107", "108", "109", "110", "110b", "110c"])

    versions = []
    for number in version_numbers:
        versions.append((number,'content/VtP/VancianToPsionicsBeta' + number + '.pdf'))

    return render_template("vtp.jinja2", sitename=u"The Vancian to Psionics Project", versions=versions, english=True)


@app.route("/bufftracker/")
def buff_tracker():
    spell_objects = spell_models.Spells.query.order_by(spell_models.Spells.id).all()
    spell_list = [spell.serialize() for spell in spell_objects]

    return render_template("bufftracker.jinja2", spell_list=spell_list, sitename=u"D&D 3.5 Buff Tracker")


'''
API routes
'''


@app.route("/api/parseMW")
def mw_parse_api():
    sheet_id = request.args.get("id", 0, type=int)

    try:
        data = Parser().get_mw_data(sheet_id)
    except:
        raise InvalidUsage("No Myth-Weavers sheet with the given ID was found", status_code=400)
    return jsonify(data)


@app.route("/api/bufftracker")
def buff_tracker_api():
    json_dict = buff_tracker_json_builder()
    return jsonify(json_dict)


def buff_tracker_json_builder():
    spells = spell_models.Spells.query.all()
    spell_list = [spell.serialize() for spell in spells]

    modifier_types = spell_models.ModifierTypes.query.all()
    modifier_list = [modifier.serialize() for modifier in modifier_types]

    numerical_bonuses = spell_models.NumericalBonuses.query.all()
    numerical_bonuses_list = [bonus.serialize() for bonus in numerical_bonuses]

    statistics = spell_models.Statistics.query.all()
    statistics_list = [statistic.serialize() for statistic in statistics]

    content = dict(spells=spell_list, modifierTypes=modifier_list, numericalBonuses=numerical_bonuses_list,
                   statistics=statistics_list)

    return dict(content=content, status=200, message="OK")
