#/usr/lib/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
from xml_parse import Parser
from errors import InvalidUsage

app = Flask(__name__)

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


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(debug=True)
