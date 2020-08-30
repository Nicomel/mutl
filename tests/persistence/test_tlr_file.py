from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import os
import sys
import pytest
import uuid
# import pytest_mock

src_dir = os.path.join(os.path.dirname(__file__), os.pardir, "")
os.path.abspath(src_dir)
sys.path.insert(0, src_dir)

from app.main import app
from app.models.task import TasksListsRepo
from app.persistence.tlr_file import TLRFile 

tst_tlr = TasksListsRepo(uuid=uuid.uuid1(), version=1)

def test_tlr_load():
    tlrFile = TLRFile()
    tlrFile.filepath = './tests/resources/mutl_data.pickle'
    tlrRepo = tlrFile.load()
    assert isinstance(tlrRepo, TasksListsRepo)