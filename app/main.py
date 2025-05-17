from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.routes import notifications

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your existing API routes
app.include_router(notifications.router)

# Mount static folder which is at root level (same level as 'app')
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend's index.html at the root URL
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("static", "index.html"))
