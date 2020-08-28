from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import os
import sys
import uuid
import datetime as dt

src_dir = os.path.join(os.path.dirname(__file__), os.pardir, "")
os.path.abspath(src_dir)
sys.path.insert(0, src_dir)

from app.main import app
from app.models.task import TasksList, Task

client = TestClient(app)
now = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
user_uuid = uuid.uuid1()

tl1 = TasksList(
    uuid = uuid.uuid1(),
    title = "TODO list 1",
    createdAt = now,
    createdBy = user_uuid,
    modifiedAt = now,
    modifiedBy = user_uuid,
)

def test_create_taskslist():
    response = client.post(
        "/taskslist/", 
        json=jsonable_encoder(tl1)
        )
    assert response.status_code == 200
    assert response.json() == {"msg": "Tasks list created"}