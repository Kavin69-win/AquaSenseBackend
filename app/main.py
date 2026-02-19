from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("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")
# Import all feature routers
# Ensure these files exist in your app/api/v1/endpoints/ folder
from app.api.v1.endpoints import (
    recommendations, 
    crops, 
    users, 
    sensors,
    villages,
    chatbot 
)

app = FastAPI(
    title="AquaSense IoT Backend",
    description="Smart Irrigation Decision Support System",
    version="1.2.0"
)

# --- 1. Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Route Registration ---
app.include_router(users.router, prefix="/api/v1/users", tags=["Farmers Management"])
app.include_router(villages.router, prefix="/api/v1/villages", tags=["Location Data"])
app.include_router(crops.router, prefix="/api/v1/crops", tags=["Crop Reference Data"])
app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["IoT Ingestion"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Irrigation Logic"])
app.include_router(chatbot.router, prefix="/api/v1/chat", tags=["AI Assistant"])

# --- 3. Base Health Check ---
@app.get("/", tags=["General"])
async def root():
    return {
        "app": "AquaSense Backend",
        "status": "Online",
        "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)