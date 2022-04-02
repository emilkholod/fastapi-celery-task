from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel


class Task(BaseModel):
    args: List[float]


class TasksSchema(BaseModel):
    task_ids: List[UUID]


class CreateTaskSchema(BaseModel):
    task_id: List[UUID]


class GetTaskStatusSchema(BaseModel):
    id: UUID
    status: str
    output: Dict
