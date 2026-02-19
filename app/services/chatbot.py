import os
from datetime import date
from groq import Groq # Switched to Groq
from dotenv import load_dotenv
import time 

load_dotenv()

# Initialize Groq Client
# Replace this with your Groq API key (gsk_...)
# Get one at: https://console.groq.com/keys
manual_key = "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"

try:
    client = Groq(api_key=manual_key)
    print("✅ AquaBot Client (Groq) initialized.")
except Exception as e:
    print(f"Failed to initialize AI client: {e}")

def ask_aquabot(message: str, device_id: str, live_data: dict = None, crop_context: dict = None):
    max_retries = 3
    retry_delay = 2 # Groq is faster, lower delay is fine

    for attempt in range(max_retries):
        try:
            # 1. Base Identity
            system_prompt = "You are AquaBot, an expert agronomist for Punjab and an AI assistant for the AquaSense IoT system.\n"
            
            # 2. Context Building (Same logic as before)
            context_text = ""
            if crop_context:
                sowing = crop_context.get('sowing_date')
                crop_name = crop_context.get('crop_name', 'Unknown Crop')
                days_old = (date.today() - sowing).days if sowing else "Unknown"
                
                context_text += f"Crop Type: {crop_name}, Age: {days_old} days, Location: Punjab.\n"

            if live_data:
                context_text += f"Moisture: {live_data.get('soil_moisture', 0) * 100}%, Temp: {live_data.get('temperature_celsius')}°C.\n"

            # 3. Expert Instructions
            instructions = (
                "Use Crop Age for growth stage. >100 days is harvest. Tone: professional/concise."
            )
            
            # Groq uses the 'Messages' format (Standard for Llama/OpenAI)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt + instructions},
                    {"role": "user", "content": f"Context: {context_text}\nQuestion: {message}"}
                ]
            )
            
            return response.choices[0].message.content

        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                print(f"⚠️ Groq Busy. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            
            return f"AquaBot encountered an error: {str(e)}"