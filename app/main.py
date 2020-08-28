from typing import Optional
from uuid import UUID

from fastapi import FastAPI
from .models.task import Task, TasksList, TasksListsRepo
from .models.user import User

app = FastAPI()

@app.post("/taskslist/")
def create_taskslist(taskslist: TasksList):
    """
    Create a tasks list
    """
    # Push taskslist creation event
    return {"msg": "Tasks list created"}

@app.post("/task/")
def create_taskslist(tluuid: UUID, task: Task):
    """
    Create a task in a tasklist
    """
    # Push task creation event
    return {"msg": "Tasks list created"}
