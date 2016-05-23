# -*- coding: utf-8 -*-

from flask import Flask, jsonify



def create_app(name="my-awesome-app"):
    app = Flask(name)

    configure_views(app)
    configure_errorhandlers(app)
    return app


def configure_views(app):
    from .view import api
    app.register_blueprint(api)


def configure_errorhandlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404