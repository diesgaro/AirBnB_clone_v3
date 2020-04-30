#!/usr/bin/python3
"""
Module status
"""


from flask import Flask, jsonify, Blueprint, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(response_or_exc):
    """Method to close the session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler error 404 and return the response in json format"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
