import uvicorn
from typing import Optional
from uuid import UUID, uuid1

import logging

from fastapi import FastAPI, Path
import pickle
# from fastapi.encoders import jsonable_encoder
from .config import mutl_config as config
from .controllers import controller as ctrl
from .models.task import Task, TasksList, TasksListsRepo
from .models.datachange import *
from .models.user import User

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging._nameToLevel[config.mutl_log_level])
logger = logging.getLogger(__name__)
logger.info("Starting MUTL services")

app = FastAPI()

@app.get("/alltaskslists/", response_model=TasksListsRepo)
async def get_all_taskslists():
    """
    Get all tasks lists
    """
    cachedTlr = ctrl.getCachedTlr()
    return cachedTlr

@app.post("/taskslist/")
async def create_taskslist(taskslist: TasksList):
    """
    Create a tasks list
    """
    # Push taskslist creation event
    creationlog = TasksListCreationLog(
        operation=Operation.CREATE, 
        objectType=ObjectType.TASKSLIST,
        serializedObject=pickle.dumps(taskslist)
        )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[creationlog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Tasks list creation submitted"}

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
    creationlog = TaskCreationLog(
        operation=Operation.CREATE, 
        objectType=ObjectType.TASK,
        tluuid=tluuid,
        pos=pos,
        serializedObject=pickle.dumps(task)
        )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[creationlog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Tasks list creation submitted"}

@app.put("/taskslist/")
async def replace_taskslist_field(
    tluuid: UUID,
    field_name: str,
    field_change: str
    ):
    """
    Replace the content of a tasks list field
    """
    updateLog = DataUpdateLog(
        operation=Operation.UPDATE, 
        objectType=ObjectType.TASKSLIST,
        tluuid=tluuid,
        fieldName=field_name,
        fieldChange=field_change
    )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[updateLog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Field replacement submittedd"}

@app.put("/task/")
async def replace_task_field(
    tluuid: UUID,
    tuuid: UUID,
    field_name: str,
    field_change: str
    ):
    """
    Replace the content of a task field
    """
    updateLog = DataUpdateLog(
        operation=Operation.UPDATE, 
        objectType=ObjectType.TASK,
        tluuid=tluuid,
        tuuid=tuuid,
        fieldName=field_name,
        fieldChange=field_change
    )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[updateLog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Field replacement submitted"}

# @app.put("/taskpriority/")
# async def update_task_priority(
#     tluuid: UUID,
#     tuuid: UUID,
#     pos: int
#     ):
#     """
#     Update task priority in a tasks list
#     """
    ctrl.pushChanges(changesList)
#     return {"msg": "Priority update submitted"}

@app.patch("/taskslist/")
async def append_taskslist_field(
    tluuid: UUID,
    field_name: str,
    field_change: str
    ):
    """
    Append the content of a tasks list field
    """
    updateLog = DataUpdateLog(
        operation=Operation.PATCH, 
        objectType=ObjectType.TASKSLIST,
        tluuid=tluuid,
        fieldName=field_name,
        fieldChange=field_change
    )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[updateLog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Field update submitted"}

@app.patch("/task/")
async def append_task_field(
    tluuid: UUID,
    tuuid: UUID,
    field_name: str,
    field_change: str
    ):
    """
    Append the content of a task field
    """
    updateLog = DataUpdateLog(
        operation=Operation.PATCH, 
        objectType=ObjectType.TASK,
        tluuid=tluuid,
        tuuid=tuuid,
        fieldName=field_name,
        fieldChange=field_change
    )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[updateLog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Field update submitted"}

@app.delete("/taskslist/")
async def delete_taskslist(
    tluuid: UUID
    ):
    """
    Delete a tasks list
    """
    deleteLog = DataDeleteLog(
        operation=Operation.DELETE, 
        objectType=ObjectType.TASKSLIST,
        tluuid=tluuid
    )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[deleteLog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Tasks deletion submitted"}

@app.delete("/task/")
async def delete_task_in_list(
    tluuid: UUID,
    tuuid: UUID
    ):
    """
    Delete a task in a list
    """
    deleteLog = DataDeleteLog(
        operation=Operation.DELETE, 
        objectType=ObjectType.TASK,
        tluuid=tluuid,
        tuuid=tuuid
    )
    changesList = DataChangesList(
        uuid=uuid1(), 
        fromRepoVersion=ctrl.getLocalRepoVersion(),
        changeLogsList=[deleteLog]
        )
    ctrl.pushChanges(changesList)
    return {"msg": "Tasks deletion submitted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)