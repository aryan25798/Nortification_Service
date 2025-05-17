from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.routes import notifications

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your existing API routes
app.include_router(notifications.router)

# Mount the static folder (serves JS, CSS, images, etc. from /static)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve your frontend's index.html at root URL
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("app", "static", "index.html"))
