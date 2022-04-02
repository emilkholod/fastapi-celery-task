from fastapi import APIRouter
from fastapi.responses import JSONResponse

import schemas
from celery.result import AsyncResult
from http_codes import CREATED_CODE, NOT_FOUND_CODE, OK_CODE
from redis_app import redis_app
from worker import create_task

router = APIRouter(prefix="/tasks")


@router.get("/", response_model=schemas.TasksSchema)
async def get_tasks():
    response_data = {
        "task_ids": [task_id.decode() for task_id in redis_app.hgetall("tasks")]
    }
    return JSONResponse(response_data)


@router.post("/create", response_model=schemas.CreateTaskSchema)
async def run_task(task_in: schemas.Task):
    task = create_task.delay(task_in.args)
    redis_app.hset("tasks", task.id, 0)
    return JSONResponse({"task_id": task.id}, status_code=CREATED_CODE)


@router.get("/{task_id}", response_model=schemas.GetTaskStatusSchema)
async def get_status(task_id):
    task = redis_app.hget("tasks", task_id)
    if task is None:
        response_data = {
            "error": "Task Not Found",
        }
        status_code = NOT_FOUND_CODE
    else:
        task = AsyncResult(task_id)
        response_data = {
            "id": task.id,
            "status": task.status,
            "output": task.result,
        }
        status_code = OK_CODE

    return JSONResponse(response_data, status_code=status_code)
