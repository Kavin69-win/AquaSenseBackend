from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Import all feature routers from your endpoints folder
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
    description="Smart Irrigation Decision Support System for Punjab Agriculture",
    version="1.2.0"
)

# --- 1. Middleware Configuration ---
# Essential for connecting your Frontend (React/Web/Mobile) to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Route Registration ---
# This links your individual feature files to the main URL structure

# Farmer Profile & Simple Login
app.include_router(
    users.router, 
    prefix="/api/v1/users", 
    tags=["Farmers Management"]
)

# Location Lists (Hoshiarpur, Bathinda, etc.)
app.include_router(
    villages.router, 
    prefix="/api/v1/villages", 
    tags=["Location Data"]
)

# Crop Catalog (Wheat, Paddy, etc.)
app.include_router(
    crops.router, 
    prefix="/api/v1/crops", 
    tags=["Crop Reference Data"]
)

# IoT Hardware Ingestion (Moisture/Temp from ESP32)
# This points to the /record logic we updated above
app.include_router(
    sensors.router, 
    prefix="/api/v1/sensors", 
    tags=["IoT Ingestion"]
)

# The "Brain" - Irrigation Decision Logic
app.include_router(
    recommendations.router, 
    prefix="/api/v1/recommendations", 
    tags=["Irrigation Logic"]
)

# AI Chatbot Assistant for Farmers
app.include_router(
    chatbot.router, 
    prefix="/api/v1/chat", 
    tags=["AI Assistant"]
)

# --- 3. Base Health Check ---
@app.get("/", tags=["General"])
async def root():
    """
    Returns the system status and current server time.
    """
    return {
        "app": "AquaSense Backend",
        "status": "Online",
        "documentation": "/docs",
        "system_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Entry point for running locally
if __name__ == "__main__":
    import uvicorn
    # Using 'app.main:app' ensures the module is loaded correctly by Uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)