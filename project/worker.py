import logging
import os
import time

import requests

from celery import Celery
from http_codes import OK_CODE

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
worldtimeapi_url = "http://worldtimeapi.org/api/timezone/Etc/UTC"

logger = logging.getLogger(__name__)


def append_time_to_result(func):
    def wrapper(*args, **kwargs):
        output = {}
        output["task_result"] = func(*args, **kwargs)
        response = requests.request("GET", worldtimeapi_url)
        if response.status_code == OK_CODE:
            output["finished_time"] = response.json()["utc_datetime"]
        else:
            output["finished_time"] = False
        return output
    return wrapper


@celery_app.task()
@append_time_to_result
def create_task(numbers):
    time.sleep(10)
    return sum(numbers)
