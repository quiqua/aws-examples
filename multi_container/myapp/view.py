# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

from .extensions import redis_store, celery
from .tasks import long_running_task



api = Blueprint("showcase_api", __name__)

@api.route("/")
def index():
    return jsonify({"message": "Hello World!"})


@api.route("/task/<name>")
def invoke_task(name):
    task = long_running_task.delay(name)
    redis_key = "my-task-{0}".format(task.id)
    # store the id and metadata about our task
    redis_store.hmset(redis_key, {u"id": task.id, u"name": name})

    return jsonify(task={"id": task.id, "state": task.state, "info": task.info})


@api.route(u"/list/all")
def list_all_tasks():
    keys = redis_store.keys(pattern="my-task-*")
    result = {}

    for key in keys:
        data = redis_store.hgetall(key)
        task_id = data.get(b"id")
        if task_id is not None:
            task = celery.AsyncResult(task_id.decode())
            result[key.decode()] = [task.state, task.info]

    return jsonify(tasks=result)