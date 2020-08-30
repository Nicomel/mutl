from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from typing import Dict, OrderedDict
import os
import sys
import pytest
# import pytest_mock
import uuid
import datetime as dt

src_dir = os.path.join(os.path.dirname(__file__), os.pardir, "")
os.path.abspath(src_dir)
sys.path.insert(0, src_dir)

from app.main import app
from app.models.task import TasksList, Task, TaskStatus, TasksListsRepo

client = TestClient(app)
now = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
user_uuid = uuid.uuid1()

tst_tlr = TasksListsRepo(uuid=uuid.uuid1(), version=1)

@pytest.fixture(autouse=True)
def initialize_tst_data():
    for i in range(1,5):
        tluuid = uuid.uuid1()
        tl = TasksList(
            uuid = tluuid,
            title = "TODO list " + str(i),
            tasks = OrderedDict(),
            createdAt = now,
            createdBy = user_uuid,
            modifiedAt = now,
            modifiedBy = user_uuid
        )
        for j in range(1,10):
            tuuid = uuid.uuid1()
            t = Task(
                uuid = tuuid,
                title = "Task " + str(j),
                description = "Task description" + str(j),
                status = TaskStatus.OPEN,
                mergeconflict = False,
                deleted = False,
                createdAt = now,
                createdBy = user_uuid,
                modifiedAt = now,
                modifiedBy = user_uuid
            )
            tl.tasks[tuuid] = t
        tst_tlr.TasksListsDict[tluuid] = tl

def test_create_taskslist():
    response = client.post(
        "/taskslist/", 
        json=jsonable_encoder(tst_tlr.TasksListsDict[list(tst_tlr.TasksListsDict)[0]])
        )
    assert response.status_code == 200
    assert response.json() == {"msg": "Tasks list created"}