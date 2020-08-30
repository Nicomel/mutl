from typing import Optional
from uuid import UUID

from fastapi import FastAPI, Path
from .models.task import Task, TasksList, TasksListsRepo
from .models.user import User

app = FastAPI()

@app.post("/taskslist/")
async def create_taskslist(taskslist: TasksList):
    """
    Create a tasks list
    """
    # Push taskslist creation event
    return {"msg": "Tasks list created"}

@app.post("/task/")
async def create_task(
    task: Task,
    tluuid: UUID, 
    pos: int = Path(0, title="Priority of the task", ge=0) 
    ):
    """
    Create a task in a tasklist
    """
    # Push task creation event
    return {"msg": "Tasks list created"}
