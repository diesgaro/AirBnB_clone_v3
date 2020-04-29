#!/usr/bin/python3
"""
Creating an Index to return the json status
"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    """Checking the status"""
    return jsonify(status='OK')