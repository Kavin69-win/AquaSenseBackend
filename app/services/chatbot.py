import os
from datetime import date
from google import genai
from dotenv import load_dotenv
import time # Needed for the retry delay

load_dotenv()

try:
    client = genai.Client()
except Exception as e:
    print(f"Failed to initialize AI client: {e}")

def ask_aquabot(message: str, device_id: str, live_data: dict = None, crop_context: dict = None):
    # Set retry parameters to handle 429 errors
    max_retries = 3
    retry_delay = 5 # seconds

    for attempt in range(max_retries):
        try:
            # 1. Base Identity
            prompt = "You are AquaBot, an expert agronomist for Punjab and an AI assistant for the AquaSense IoT system.\n"
            
            # 2. Inject Crop & User Context (THE SMART PART)
            if crop_context:
                sowing = crop_context.get('sowing_date')
                crop_name = crop_context.get('crop_name', 'Unknown Crop')
                
                # Calculate Age
                days_old = (date.today() - sowing).days if sowing else "Unknown"
                
                prompt += f"--- CROP CONTEXT ---\n"
                prompt += f"Crop Type: {crop_name}\n"
                prompt += f"Sowing Date: {sowing}\n"
                prompt += f"Crop Age: {days_old} days\n"
                prompt += f"Location: Punjab, India\n"
                prompt += "--------------------\n\n"

            # 3. Inject Sensor Data
            if live_data:
                prompt += f"--- LIVE SENSOR DATA ---\n"
                prompt += f"Soil Moisture: {live_data.get('soil_moisture', 0) * 100}%\n"
                prompt += f"Temperature: {live_data.get('temperature_celsius', 'Unknown')}°C\n"
                prompt += f"Humidity: {live_data.get('humidity_percent', 'Unknown')}%\n"
                prompt += "------------------------\n\n"
            
            prompt += f"Farmer Question: '{message}'\n\n"
            
            # 4. Expert Instructions
            prompt += (
                "INSTRUCTIONS:\n"
                "- Use the Crop Age to determine the growth stage (Seedling, Vegetative, or Harvesting).\n"
                "- If the crop is >100 days old, it's likely nearing harvest; advise accordingly.\n"
                "- Keep the tone helpful, professional, and concise."
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite', 
                contents=prompt,
            )
            return response.text

        except Exception as e:
            # Detect Rate Limit Error
            if "429" in str(e) and attempt < max_retries - 1:
                print(f"⚠️ AquaBot Busy (429). Retrying in {retry_delay}s... (Attempt {attempt + 1})")
                time.sleep(retry_delay)
                retry_delay *= 2 # Wait longer on next try (Exponential Backoff)
                continue
            
            return f"AquaBot encountered an error: {str(e)}"