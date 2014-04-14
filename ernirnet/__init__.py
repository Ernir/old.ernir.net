from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
import os

from ernirnet.helpers.bufftracker.xml_parse import Parser

from ernirnet.helpers.errors import InvalidUsage


app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(os.path.abspath(os.path.dirname(__file__)), "tmp"))

from ernirnet import views
import ernirnet.helpers.bufftracker.spell_models

'''
Error handlers
'''

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
