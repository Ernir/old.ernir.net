from flask import Flask, jsonify
from ernirnet.xml_parse import Parser
from ernirnet.errors import InvalidUsage

app = Flask(__name__)

from ernirnet import views

'''
Error handlers
'''

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
