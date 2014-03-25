from flask import Flask, jsonify
from ernirnet.xml_parse import Parser
from ernirnet.errors import InvalidUsage
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_BINDS"] = {"blog" : "sqlite:///db/blog.db", "spells" : "sqlite:///db/spells.db"}

db = SQLAlchemy(app)

from ernirnet import views
import ernirnet.spell_models

'''
Error handlers
'''

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
