from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Notification(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: int
    type: str  # "email", "sms", "in-app"
    message: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
