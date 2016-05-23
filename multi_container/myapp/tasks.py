# -*- coding: utf-8 -*-

import time

from celery import states
from celery.exceptions import Ignore

from .extensions import celery, redis_store


@celery.task(bind=True)
def long_running_task(self, name):
    redis_key = "celery-locks-{0}".format(name)
    lock = redis_store.lock(redis_key)
    has_lock = False
    try:
        has_lock = lock.acquire(blocking=False)
        if has_lock:
                label = "Processing {0}".format(name)
                self.update_state(state=u"IN PROGRESS", meta=label)

                x = 10
                while x > 0:
                    x = x - 1
                    time.sleep(1)

        else:
            label = "Task {0} is processed by another worker.".format(name)
            self.update_state(state=states.FAILURE, meta=label)
            raise Ignore()
    finally:
        if has_lock:
            lock.release()
            return "Finished with {0}. Phew!".format(name)
