import os
from datetime import date
from openai import OpenAI  # Groq uses the OpenAI structure
from dotenv import load_dotenv
import time 
# --- CENTRAL SETTINGS ---
from app.core.config import settings 

# 1. Load environment variables
load_dotenv()

# --- UPDATED SECTION ---
# Now pulling from GROQ_API_KEY (starts with gsk_...)
api_key = settings.GROQ_API_KEY.get_secret_value()

# 2. Initialize Groq Client
try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1", # Critical for Groq
        api_key=api_key
    )
    print("✅ AquaBot Client (Groq LPU) initialized.")
except Exception as e:
    print(f"❌ Failed to initialize Groq client: {e}")

def ask_aquabot(message: str, device_id: str, live_data: dict = None, crop_context: dict = None):
    # Llama 3.3 70B is Groq's best balance of high intelligence and speed
    model_name = "llama-3.3-70b-versatile"
    
    max_retries = 2
    retry_delay = 1 # Groq is fast, shorter delay is fine

    for attempt in range(max_retries):
        try:
            # 1. Base Identity & Context
            system_prompt = "You are AquaBot, an expert agronomist for Punjab and an AI assistant for the AquaSense IoT system."
            
            context_text = ""
            if crop_context:
                sowing = crop_context.get('sowing_date')
                crop_name = crop_context.get('crop_name', 'Unknown Crop')
                try:
                    days_old = (date.today() - sowing).days if sowing else "Unknown"
                except Exception:
                    days_old = "Unknown"
                context_text += f"Crop Type: {crop_name}, Age: {days_old} days, Location: Punjab.\n"

            if live_data:
                moisture = live_data.get('soil_moisture', 0)
                temp = live_data.get('temperature_celsius', 'N/A')
                context_text += f"Moisture: {moisture * 100}%, Temp: {temp}°C.\n"

            instructions = "Use Crop Age for growth stage. >100 days is harvest. Tone: professional/concise."
            
            # 2. Groq API Call
            # We use the standard chat.completions structure
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": f"{system_prompt}\n{instructions}"},
                    {"role": "user", "content": f"Context: {context_text}\nQuestion: {message}"}
                ]
            )
            
            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ Groq attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                return "AquaBot is currently resting (Groq Limit). Please try again in a moment."

    return "AquaBot is currently resting."