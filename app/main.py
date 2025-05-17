from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import notifications

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notifications.router)

@app.get("/")
def health_check():
    return {"status": "Notification service is running"}
