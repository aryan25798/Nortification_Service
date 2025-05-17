from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, rabbitmq
from app.utils import is_valid_notification_type
import time

router = APIRouter()

def simulate_delivery_and_mark_sent(db: Session, notification_id: int):
    time.sleep(1)
    notification = db.query(models.Notification).get(notification_id)
    if notification:
        notification.status = "sent"
        db.commit()

@router.post("/notifications", response_model=schemas.NotificationResponse)
async def send_notification(
    notification: schemas.NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if not is_valid_notification_type(notification.type):
        raise HTTPException(status_code=400, detail="Invalid notification type")

    db_notification = models.Notification(**notification.dict(), status="pending")
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    await rabbitmq.publish_notification({"id": db_notification.id})
    background_tasks.add_task(simulate_delivery_and_mark_sent, db, db_notification.id)

    return db_notification

@router.get("/users/{user_id}/notifications", response_model=list[schemas.NotificationResponse])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).all()

@router.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"detail": "Notification deleted successfully"}
