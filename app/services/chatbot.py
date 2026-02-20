from datetime import date
from groq import AsyncGroq
from app.core.config import settings

# Initialize Groq client using environment config
# This assumes GROQ_API_KEY is set either in:
# - .env (local)
# - Render Environment Variables (production)

def get_groq_client():
    return AsyncGroq(
        api_key=settings.GROQ_API_KEY.get_secret_value()
    )

async def ask_aquabot(
    message: str,
    device_id: str,
    live_data: dict = None,
    crop_context: dict = None
):
    """
    AquaBot powered by Groq LPU (Ultra-fast inference).
    """

    model_name = "llama-3.3-70b-versatile"
    client = get_groq_client()

    # Base identity
    system_prompt = (
        "You are AquaBot, an expert agronomist for Punjab "
        "and an AI assistant for the AquaSense IoT system."
    )

    context_text = ""

    if crop_context:
        sowing = crop_context.get("sowing_date")
        crop_name = crop_context.get("crop_name", "Unknown Crop")

        try:
            days_old = (date.today() - sowing).days if sowing else "Unknown"
        except Exception:
            days_old = "Unknown"

        context_text += (
            f"Crop Type: {crop_name}, "
            f"Age: {days_old} days, "
            f"Location: Punjab.\n"
        )

    if live_data:
        moisture = live_data.get("soil_moisture", 0)
        temp = live_data.get("temperature_celsius", "N/A")

        context_text += (
            f"Moisture: {moisture * 100:.1f}%, "
            f"Temp: {temp}°C.\n"
        )

    instructions = (
        "Use Crop Age for growth stage analysis. "
        ">100 days is harvest stage. "
        "Tone: professional and concise."
    )

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{system_prompt}\n{instructions}"
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_text}\n\nQuestion:\n{message}"
                }
            ],
            model=model_name,
            temperature=0.2,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"❌ Groq API Error: {str(e)}")
        return (
            "AquaBot is currently analyzing satellite data. "
            "Please try again in 30 seconds."
        )