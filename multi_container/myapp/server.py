# -*- coding: utf-8 -*-

from flask import Flask, jsonify

from .extensions import celery, redis_store

import logging

def create_app(name="my-awesome-app"):
    app = Flask(name)

    app.config.update(
        REDIS_URL="redis://redis:6379",
        CELERY_BROKER_URL="redis://redis:6379",
        CELERY_RESULT_BACKEND="redis://redis:6379"
    )

    configure_extensions(app)
    configure_logging(app)
    configure_views(app)
    configure_errorhandlers(app)
    return app, celery


def configure_extensions(app):
    redis_store.init_app(app)
    celery.init_app(app)


def configure_views(app):
    from .view import api
    app.register_blueprint(api)


def configure_errorhandlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404


def configure_logging(app):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
