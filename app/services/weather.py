import requests
from typing import Tuple

# Replace with your actual key
API_KEY = "fda377b4ab9cbffc67abc8852bac131b"

def get_rain_forecast(village_name: str) -> Tuple[bool, float]:
    """
    Returns (Will_Rain, Probability) for the next 3 hours.
    """
    try:
        # Search forecast for the village (or nearest district like Hoshiarpur)
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={village_name},IN&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return False, 0.0

        # Look at the first entry (the next 3-hour window)
        next_3h = data['list'][0]
        prob_of_precipitation = next_3h.get('pop', 0) # 'pop' is probability (0 to 1)
        
        # Decision: If probability > 60%, we call it "Likely to Rain"
        will_rain = prob_of_precipitation >= 0.6
        return will_rain, prob_of_precipitation
    except:
        return False, 0.0