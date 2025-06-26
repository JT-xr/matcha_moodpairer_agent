# cafe_search.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def search_matcha_cafes(location: str, radius=3000):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": f"matcha cafe near {location}",
        "radius": radius,
        "key": GOOGLE_PLACES_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    cafes = []
    for place in data.get("results", []):
        cafes.append({
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating"),
            "map_link": f"https://maps.google.com/?q={place.get('name').replace(' ', '+')}",
        })

    return cafes