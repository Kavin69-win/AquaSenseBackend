import os
import json
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Gemini Client
# NOTE: Ensure "AIzaSy..." is your actual NEW key from a fresh Google account.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def calculate_soil_threshold(crop_name: str, soil_type: str, growth_stage: str):
    """
    AI Logic Engine: Optimized for Gemini 2.0 Flash-Lite with robust error handling.
    """
    prompt = f"""
    ACT AS A PRECISION AG-LOGIC ENGINE.
    CONTEXT: Punjab Agriculture geography.
    INPUTS: Crop: {crop_name}, Soil: {soil_type}, Stage: {growth_stage}.
    TASK: Calculate optimal soil moisture threshold (0.0 to 1.0) for an ESP32 pump trigger.
    
    TECHNICAL RULES: 
    - Sandy/Desert: Needs high threshold (~0.45) due to zero retention.
    - Clay: Needs low threshold (~0.20) to prevent water-logging.
    - Alluvial/Loam: Needs balanced threshold (~0.32).
    - Kandi Hill: Needs moderate-high (~0.35) due to runoff.

    OUTPUT FORMAT: Return ONLY a raw JSON object. No conversational text.
    FORMAT: {{"threshold": float, "reason": "string"}}
    """
    
    try:
        # Re-integrating Gemini 2.0 Flash-Lite
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite', 
            contents=prompt
        )
        
        # DEBUG: This is your best friend in the terminal right now
        print(f"--- AI RAW RESPONSE ---\n{response.text}\n-----------------------")

        # CLEANING LOGIC: Removes markdown if the AI includes it
        clean_json = response.text.strip()
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()

        # PARSING: Convert string to dictionary
        return json.loads(clean_json)

    except Exception as e:
        # EXPLICIT ERROR LOGGING: Look for this in your terminal to see WHY it's offline
        print(f"CRITICAL AI ERROR: {str(e)}") 
        
        soil_lower = soil_type.lower()
        
        # SMART FALLBACK LOGIC
        if "sandy" in soil_lower or "desert" in soil_lower:
            smart_val = 0.45
            reason = "Offline Logic: Arid/Sandy soil requires high threshold for frequent irrigation."
        elif "kandi" in soil_lower:
            smart_val = 0.35
            reason = "Offline Logic: Kandi Hill soil prone to runoff; moderate-high threshold."
        elif "clay" in soil_lower:
            smart_val = 0.20
            reason = "Offline Logic: Clay content retains moisture; low threshold to prevent rot."
        elif "loam" in soil_lower or "alluvial" in soil_lower:
            if "sandy loam" in soil_lower:
                smart_val = 0.38
            else:
                smart_val = 0.32
            reason = f"Offline Logic: Optimized moisture for {soil_type} in Central Punjab."
        elif "calcareous" in soil_lower:
            smart_val = 0.30
            reason = "Offline Logic: Balanced threshold for salt-rich Calcareous soil."
        else:
            smart_val = 0.25
            reason = f"Offline Logic: Default safety threshold for {soil_type}."

        return {"threshold": smart_val, "reason": reason}