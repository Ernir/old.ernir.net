from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from ernirnet.helpers.bufftracker.xml_parse import Parser

from ernirnet.helpers.errors import InvalidUsage


app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)

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
