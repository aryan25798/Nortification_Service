from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import notifications
import asyncio
from app.notifier import process_notifications
from app.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Notification Service")

# Enable CORS (modify origins as needed in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(notifications.router)

# Run the notification processor on startup
@app.on_event("startup")
async def startup():
    asyncio.create_task(process_notifications())

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "Notification service is running"}
