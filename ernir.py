#/usr/lib/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, render_template

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

@app.route("/kennsla/")
def kennsla():
    return None

if __name__ == "__main__":
    app.run(debug=True)
