from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    type: str  # "email", "sms", or "in-app"
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    message: str
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
