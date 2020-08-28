from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

class User(BaseModel):
    """
    This is the description of the user model
    """
    uuid: UUID = Field(...,title="UUID", description="Unique identifier")
    firstName: str = Field(..., title="First Name", description= "First Name of the user")
    lastName: str = Field(..., title="Last Name", description= "Last Name of the user")
    Scope: Optional[int]
    createdAt: datetime = Field(...,title="Created At", description="Creation time")