from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID

class TaskStatus(str, Enum):
    open = 'open'
    inprogress = 'in progress'
    blocked = 'blocked'
    completed = 'completed'

class Task(BaseModel):
    """
    This is the description of the task model
    """
    uuid: UUID = Field(...,title="UUID", description="Unique identifier")
    # priority: int = Field(..., title="Priority", description= "Priority of the task")
    title: str = Field(..., title="Title", description= "Title of the task")
    description: Optional[str] = Field(
        None, title="The description of the task", max_length=300
    )
    status: TaskStatus = Field(
        TaskStatus.open, title="Status",  description= "Status of the task"
    )
    mergeconflict: Optional[bool] = Field(
        False, title="Merge confict flag", description= "Flag if manual reconciliation required"
    )
    deleted: Optional[bool] = Field(
        False, title="Deleted flag",  description= "Flag to indicate if the task is deleted"
    )
    createdAt: datetime = Field(...,title="Created At", description="Creation time")
    createdBy: UUID = Field(...,title="UUID", description="Unique identifier of the User")
    modifiedAt: datetime = Field(...,title="Modified At", description="Modification time")
    modifiedBy: UUID = Field(...,title="UUID", description="Unique identifier of the User")

class TasksList(BaseModel):
    """
    This is the description of the tasks list model
    """
    uuid: UUID = Field(...,title="UUID", description="Unique identifier")
    title: str = Field(..., title="Title", description= "Title of the task")
    tasks: Optional[List[Task]] = []
    createdAt: datetime = Field(...,title="Created At", description="Creation time")
    createdBy: UUID = Field(...,title="UUID", description="Unique identifier of the User")
    modifiedAt: datetime = Field(...,title="Modified At", description="Modification time")
    modifiedBy: UUID = Field(...,title="UUID", description="Unique identifier of the User")
    
class TasksListsRepo(BaseModel):
    """
    This is the description of the tasks lists repository model
    """
    uuid: UUID = Field(...,title="UUID", description="Unique identifier")
    version: int = Field(..., title="Version", description= "Version number")
    TasksListsDict: Optional[Dict[UUID,TasksList]] = {}