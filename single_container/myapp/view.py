# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

api = Blueprint("showcase_api", __name__)

@api.route("/")
def index():
    return jsonify({"message": "Hello World!"})