# mood_drink_map.py

def get_drink_for_mood(mood: str) -> str:
    mood = mood.lower()
    mapping = {
        "chill": "Iced matcha latte with oat milk",
        "anxious": "Warm hojicha tea – calming and low caffeine",
        "creative": "Matcha with lavender or rose syrup",
        "reflective": "Hot matcha latte with almond milk",
        "energized": "Matcha lemonade – fresh and zesty",
        "cozy": "Warm ceremonial matcha with oat milk",
    }
    return mapping.get(mood, "Classic matcha latte")