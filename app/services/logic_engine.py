import os
import json
from groq import Groq # Switched from genai to groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq Client
# Ensure you have GROQ_API_KEY=gsk_... in your .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def calculate_soil_threshold(crop_name: str, soil_type: str, growth_stage: str):
    """
    AI Logic Engine powered by Groq (Llama 3).
    """
    prompt = f"""
    Return ONLY a raw JSON object for an irrigation system. 
    INPUT: Crop: {crop_name}, Soil: {soil_type}, Stage: {growth_stage}.
    FORMAT: {{"threshold": float, "reason": "string"}}
    """
    
    try:
        # Using Llama 3 on Groq for ultra-fast response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a precision agriculture logic engine."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # Forces JSON output
        )
        
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"DEBUG ERROR: {e}") 
        soil_lower = soil_type.lower()
        
        # --- HARDCODED SMART FALLBACK (Same as before) ---
        if "sandy" in soil_lower:
            smart_val, reason = 0.45, "Offline: Sandy soil needs high frequency."
        elif "clay" in soil_lower:
            smart_val, reason = 0.20, "Offline: Clay retains water; low threshold."
        else:
            smart_val, reason = 0.32, f"Offline: Standard threshold for {soil_type}."

        return {"threshold": smart_val, "reason": reason}