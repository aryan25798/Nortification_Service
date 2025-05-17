from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    type: str
    message: str

class NotificationResponse(BaseModel):
    id: str
    user_id: int
    type: str
    message: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
