import os
import json
  # Use native Groq Async client
from pydantic import BaseModel
from dotenv import load_dotenv
# --- CENTRAL SETTINGS ---
from app.core.config import settings 

load_dotenv()

# 1. Initialize Direct Groq Client
# Ensure your .env has: GROQ_API_KEY=gsk_...



# 2. Define the response structure for documentation/safety
class ThresholdResponse(BaseModel):
    threshold: float
    reason: str

async def calculate_soil_threshold(crop_name: str, soil_type: str, growth_stage: str):
    """
    AI Logic Engine powered by Groq LPU.
    Calculates the optimal soil moisture threshold for irrigation.
    """
    
    # We specify JSON instructions in the prompt for Llama 3.3
    prompt = f"""
    Return a JSON object for an irrigation system. 
    INPUT: Crop: {crop_name}, Soil: {soil_type}, Stage: {growth_stage}.
    FORMAT: {{"threshold": float, "reason": "string"}}
    """

    try:
        # Groq's LPU is ultra-fast. We use JSON mode here.
        chat_completion = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a precision agriculture logic engine. You must output valid JSON."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            # This ensures Groq returns a structured JSON object
            response_format={"type": "json_object"}
        )
        
        ai_response = chat_completion.choices[0].message.content
        return json.loads(ai_response)

    except Exception as e:
        print(f"⚠️ Groq Logic Engine failed: {e}")
        
        # --- FINAL HARDCODED FALLBACK (Your Safety Net) ---
        print("🚨 Using Hardcoded Safety Logic.")
        soil_lower = soil_type.lower()
        if "sandy" in soil_lower:
            smart_val, reason = 0.45, "Offline: Sandy soil needs high frequency."
        elif "clay" in soil_lower:
            smart_val, reason = 0.20, "Offline: Clay retains water; low threshold."
        else:
            smart_val, reason = 0.32, f"Offline: Standard threshold for {soil_type}."

        return {"threshold": smart_val, "reason": reason}