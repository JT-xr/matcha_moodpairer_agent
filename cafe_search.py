# cafe_search.py

import requests
import os
from dotenv import load_dotenv
from telemetry import langfuse
from langfuse import observe, get_client

load_dotenv()
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

@observe(name="api.googlemaps_search_matcha_cafes", as_type="tool")
def search_matcha_cafes(location: str, radius=3500):
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
        # Get additional details if place_id is available
        place_id = place.get("place_id")
        phone = None
        website = None
        
        # Get place details for phone number and more info
        if place_id and GOOGLE_PLACES_API_KEY:
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "fields": "formatted_phone_number,website,business_status,price_level",
                "key": GOOGLE_PLACES_API_KEY,
            }
            try:
                details_response = requests.get(details_url, params=details_params)
                details_data = details_response.json()
                if details_data.get("status") == "OK":
                    result = details_data.get("result", {})
                    phone = result.get("formatted_phone_number")
                    website = result.get("website")
            except:
                pass  # Continue without details if API call fails
        
        cafes.append({
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating"),
            "phone": phone,
            "website": website,
            "place_id": place_id,
            "map_link": f"https://maps.google.com/?q={place.get('name').replace(' ', '+')}",
        })

    return cafes

langfuse = get_client()
langfuse.flush()