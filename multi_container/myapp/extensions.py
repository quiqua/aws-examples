# -*- coding: utf-8 -*-

from flask.ext.celery import Celery
from flask.ext.redis import FlaskRedis

celery = Celery()

redis_store = FlaskRedis()
