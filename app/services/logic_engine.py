import json
from groq import AsyncGroq
from pydantic import BaseModel

from app.core.config import settings


# ===== Response Schema =====
class ThresholdResponse(BaseModel):
    threshold: float
    reason: str


# ===== Lazy Groq Client (Safe) =====
def get_groq_client():
    if not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not configured")

    return AsyncGroq(
        api_key=settings.GROQ_API_KEY.get_secret_value()
    )


# ===== AI Logic Engine =====
async def calculate_soil_threshold(
    crop_name: str,
    soil_type: str,
    growth_stage: str
):
    """
    AI-powered irrigation threshold calculator.
    Uses Groq Llama 3.3 70B.
    """

    client = get_groq_client()

    prompt = f"""
Return a JSON object for an irrigation system.

INPUT:
Crop: {crop_name}
Soil: {soil_type}
Growth Stage: {growth_stage}

FORMAT:
{{
  "threshold": float between 0.15 and 0.60,
  "reason": "short agronomy explanation"
}}
"""

    try:
        chat_completion = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precision agriculture irrigation engine. "
                        "You must return strictly valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        ai_response = chat_completion.choices[0].message.content
        parsed = json.loads(ai_response)

        # Safety validation
        threshold = float(parsed.get("threshold", 0.32))
        threshold = max(0.15, min(0.60, threshold))  # Clamp range

        return {
            "threshold": threshold,
            "reason": parsed.get("reason", "AI generated threshold")
        }

    except Exception as e:
        print(f"⚠️ Groq Logic Engine failed: {e}")
        print("🚨 Using Hardcoded Safety Logic.")

        soil_lower = soil_type.lower()

        if "sandy" in soil_lower:
            smart_val, reason = 0.45, "Offline fallback: Sandy soil drains fast."
        elif "clay" in soil_lower:
            smart_val, reason = 0.20, "Offline fallback: Clay retains water."
        else:
            smart_val, reason = 0.32, f"Offline fallback: Standard threshold for {soil_type}."

        return {
            "threshold": smart_val,
            "reason": reason
        }