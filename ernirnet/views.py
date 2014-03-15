from flask import render_template, jsonify, request
from ernirnet.xml_parse import Parser
from ernirnet import app
from ernirnet.errors import InvalidUsage

@app.route("/")
def heim():
    return render_template("index.html", sitename=u"Heim")

@app.route("/ferilskra/")
def ferilskra():
    return render_template("ferilskra.html", sitename=u"CV")

@app.route("/hafasamband/")
def samband():
    return render_template("hafasamband.html", sitename=u"Hafa samband")

@app.route("/forritun/") #TODO Do
def forritun():
    return None

@app.route("/kennsla/") #TODO Do
def kennsla():
    return None

@app.route("/api/parseMW")
def mw_parse():
    sheet_id = request.args.get("id",0,type=int)

    try:
        data = Parser().get_mw_data(sheet_id)
    except:
        raise InvalidUsage("No Myth-Weavers sheet with the given ID was found", status_code=400)
    return jsonify(data)