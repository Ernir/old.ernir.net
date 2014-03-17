from flask import render_template, jsonify, request
from ernirnet.xml_parse import Parser
from ernirnet import app
from ernirnet.errors import InvalidUsage
import spell_models


@app.route("/")
def heim():
    return render_template("index.jinja2", sitename=u"Heim")


@app.route("/ferilskra/")
def ferilskra():
    return render_template("ferilskra.jinja2", sitename=u"CV")


@app.route("/hafasamband/")
def samband():
    return render_template("hafasamband.jinja2", sitename=u"Hafa samband")


@app.route("/forritun/") #TODO Do
def forritun():
    return None


@app.route("/kennsla/") #TODO Do
def kennsla():
    return None


@app.route("/bufftracker")
def buff_tracker():
    spell_objects = spell_models.Spells.query.order_by(spell_models.Spells.id).all()
    print(spell_objects)
    spell_list = [spell.serialize() for spell in spell_objects]
    print(spell_list)
    return render_template("bufftracker.jinja2", spell_list=spell_list)


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

    content = dict(spells=spell_list, modifierTypes=modifier_list, numericalBonuses=numerical_bonuses_list)

    return dict(content=content, status=200, message="OK")
