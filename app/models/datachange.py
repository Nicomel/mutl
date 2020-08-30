
import abc
from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID

class Operation(str, Enum):
    CREATE = 'create'
    UPDATE = 'update'
    PATCH = 'patch'
    DELETE = 'delete'

class ObjectType(str, Enum):
    TASK = 'task'
    TASKSLIST = 'taskslist'

class DataChangeLog(BaseModel, abc.ABC):
    """
    This is the abstratct class to represent a data change
    """
    operation: Operation = Field(..., title="Operation", description="Operation applied to the type of object")
    objectType: ObjectType = Field(..., title="Object type", description="Type of object related to the data change")

class DataChangesList(DataChangeLog):
    """
    This is the actual class to represent a list of changes
    """
    uuid: UUID = Field(...,title="UUID", description="Unique object identifier")
    fromRepoVersion: int = Field(..., title="Based version", description= "Based version to apply the changes on")
    changeLogsList: List[DataChangeLog]

class DataCreationLog(DataChangeLog):
    """
    This is the actual class to represent a data creation
    """
    jsonObject: str = Field(...,title="JSON object", description="JSON object to be created")

class DataUpdateLog(DataChangeLog):
    """
    This is the actual class to represent a data update
    """
    uuid: UUID = Field(...,title="UUID", description="Unique object identifier")
    fieldName: str = Field(..., title="Name of the field", description= "Name of the field to be updated")
    fieldChange: str = Field(..., title="Updated string", description= "String to replace/append the field content")

class DataDeleteLog(DataChangeLog):
    """
    This is the actual class to represent a data deletion
    """
    uuid: UUID = Field(...,title="UUID", description="Unique object identifier")
