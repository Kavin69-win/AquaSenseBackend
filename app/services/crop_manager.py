from datetime import datetime, timezone

class CropManager:
    """
    Biological Intelligence Layer.
    Maps days after sowing (DAS) to physiological growth stages for Punjab crops.
    """
    # Scientific data for Wheat (Triticum aestivum) in Northern India
    CROP_STAGES = {
        "Wheat": [
            {"name_en": "Initial (CRI)", "name_hi": "ताज जड़ की शुरुआत (CRI)", "start_day": 0, "end_day": 25, "multiplier": 1.2},
            {"name_en": "Tillering", "name_hi": "कल्ले निकलना (Tillering)", "start_day": 26, "end_day": 50, "multiplier": 1.0},
            {"name_en": "Jointing", "name_hi": "गांठ बनना (Jointing)", "start_day": 51, "end_day": 75, "multiplier": 1.1},
            {"name_en": "Flowering/Milking", "name_hi": "फूल और दूधिया अवस्था", "start_day": 76, "end_day": 105, "multiplier": 1.4},
            {"name_en": "Maturity", "name_hi": "परिपक्वता", "start_day": 106, "end_day": 160, "multiplier": 0.8}
        ]
    }

    def get_stage_info(self, crop_type: str, sowing_date: datetime) -> dict:
        """
        Calculates the current growth stage based on the sowing date.
        """
        if sowing_date.tzinfo is None:
            sowing_date = sowing_date.replace(tzinfo=timezone.utc)
            
        # Calculate Days After Sowing (DAS)
        das = (datetime.now(timezone.utc) - sowing_date).days
        
        # Get stages for the crop, default to Wheat
        stages = self.CROP_STAGES.get(crop_type, self.CROP_STAGES["Wheat"])
        
        for stage in stages:
            if stage["start_day"] <= das <= stage["end_day"]:
                return {**stage, "das": das}
        
        # Default to the final stage if DAS exceeds the defined periods
        return {**stages[-1], "das": das}

# Singleton instance to be used across the app
crop_manager = CropManager()