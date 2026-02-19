import os
import json
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Initialize Gemini Client using your API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def calculate_soil_threshold(crop_name: str, soil_type: str, growth_stage: str):
    """
    The Internal AI: Takes DB values and returns a hardware threshold.
    """
    prompt = f"""
    ACT AS A PRECISION AG-LOGIC ENGINE.
    CONTEXT: Punjab Agriculture.
    INPUTS: Crop: {crop_name}, Soil: {soil_type}, Stage: {growth_stage}.
    TASK: Calculate the optimal soil moisture threshold (0.0 to 1.0) for an ESP32 pump trigger.
    RULES: 
    - Sandy soil: Needs higher threshold (~0.40) due to low retention.
    - Clay soil: Needs lower threshold (~0.22) to avoid waterlogging.
    - Growth Stage: Seedlings need more frequent water than mature crops.
    RETURN ONLY JSON: {{"threshold": float, "reason": "short explanation"}}
    """
    
    try:
        # Use Flash-Lite for speed and high quota
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite', 
            contents=prompt
        )
        
        # 1. DEBUG PRINT: See exactly what the AI says in your terminal
        print(f"--- AI RAW RESPONSE ---\n{response.text}\n-----------------------")

        # 2. CLEANING LOGIC: Handle markdown backticks or extra text
        clean_json = response.text.strip()
        if "```json" in clean_json:
            clean_json = clean_json.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_json:
            clean_json = clean_json.split("```")[1].split("```")[0].strip()

        # 3. PARSING: Convert string to dictionary
        return json.loads(clean_json)

    except Exception as e:
        # ✅ Indented correctly to stay within the function
        print(f"DEBUG ERROR: {e}") 
        # Fallback to safety default
        return {"threshold": 0.25, "reason": f"AI Parsing Error: {str(e)}"}