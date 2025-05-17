from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.database import db
from app.schemas import NotificationCreate, NotificationResponse
from bson import ObjectId
from datetime import datetime
import asyncio

router = APIRouter()
notifications_collection = db.notifications

async def simulate_delivery_and_mark_sent(notification_id: str):
    await asyncio.sleep(1)  # simulate sending delay
    await notifications_collection.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"status": "sent"}}
    )

@router.post("/notifications", response_model=NotificationResponse)
async def send_notification(notification: NotificationCreate, background_tasks: BackgroundTasks):
    notification_dict = notification.dict()
    notification_dict["status"] = "pending"
    notification_dict["created_at"] = datetime.utcnow()

    result = await notifications_collection.insert_one(notification_dict)
    notification_id = result.inserted_id

    background_tasks.add_task(simulate_delivery_and_mark_sent, str(notification_id))

    created_notification = await notifications_collection.find_one({"_id": notification_id})
    return NotificationResponse(**created_notification, id=str(created_notification["_id"]))

@router.get("/users/{user_id}/notifications", response_model=list[NotificationResponse])
async def get_user_notifications(user_id: int):
    notifications_cursor = notifications_collection.find({"user_id": user_id})
    notifications = []
    async for doc in notifications_cursor:
        notifications.append(NotificationResponse(**doc, id=str(doc["_id"])))
    return notifications

@router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: str):
    result = await notifications_collection.delete_one({"_id": ObjectId(notification_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"detail": "Notification deleted successfully"}
