
import abc
from typing import List, Dict, Optional, TypeVar
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID
from .task import Task, TasksList

class Operation(str, Enum):
    CREATE = 'create'
    UPDATE = 'update'
    PATCH = 'patch'
    DELETE = 'delete'

class ObjectType(str, Enum):
    TASK = 'Task'
    TASKSLIST = 'TasksList'

# TaskOrList = TypeVar('TaskOrList', Task, TasksList)

class DataChangeLog(BaseModel, abc.ABC):
    """
    This is the abstratct class to represent a data change
    """
    operation: Operation = Field(..., title="Operation", description="Operation applied to the type of object")
    objectType: ObjectType = Field(..., title="Object type", description="Type of object related to the data change")

class DataChangesList(BaseModel):
    """
    This is the actual class to represent a list of changes
    """
    uuid: UUID = Field(...,title="UUID", description="Unique object identifier")
    fromRepoVersion: int = Field(..., title="Based version", description= "Based version to apply the changes on")
    changeLogsList: List[DataChangeLog]

class TasksListCreationLog(DataChangeLog):
    """
    This is the actual class to represent a data creation
    """
    serializedObject: bytes = Field(...,title="Serialized object", description="Serialized object to be created")
    # createdObject: TaskOrList

class TaskCreationLog(DataChangeLog):
    """
    This is the actual class to represent a data creation
    """
    tluuid: UUID = Field(...,title="UUID", description="Unique tasks list identifier")
    pos: int = Field(0, title="Priority of the task", ge=0) 
    serializedObject: bytes = Field(...,title="Serialized object", description="Serialized object to be created")

class DataUpdateLog(DataChangeLog):
    """
    This is the actual class to represent a data update
    """
    tluuid: UUID = Field(...,title="UUID", description="Unique object identifier")
    tuuid: Optional[UUID] = Field(None, title="UUID", description="Unique object identifier")
    fieldName: str = Field(..., title="Name of the field", description= "Name of the field to be updated")
    fieldChange: str = Field(..., title="Updated string", description= "String to replace/append the field content")

class DataDeleteLog(DataChangeLog):
    """
    This is the actual class to represent a data deletion
    """
    tluuid: UUID = Field(...,title="UUID", description="Unique object identifier")
    tuuid: Optional[UUID] = Field(None, title="UUID", description="Unique object identifier")
