import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("GOOGLE_VERTEX_API_KEY")

if not API_KEY:
    print("Error: GOOGLE_VERTEX_API_KEY not found in environment variables.")
    print("Please create a .env file in the same directory and add your API key:")
    print("GOOGLE_VERTEX_API_KEY='YOUR_API_KEY_HERE'")
    exit()

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"

prompt = "Generate an image of a cozy matcha latte in a white ceramic cup on a wooden table with warm lighting."
output_filename = "matcha_latte.png"

print(f"Attempting to generate image with prompt: '{prompt}'")
print(f"Output image will be saved as: {output_filename}")

payload = {
    "instances": {
        "prompt": prompt
    },
    "parameters": {
        "sampleCount": 1
    }
}

try:
    request_url = f"{API_URL}?key={API_KEY}"
    response = requests.post(request_url, json=payload)
    response.raise_for_status()
    result = response.json()

    if result and result.get("predictions") and len(result["predictions"]) > 0:
        base64_image_data = result["predictions"][0].get("bytesBase64Encoded")

        if base64_image_data:
            image_bytes = base64.b64decode(base64_image_data)
            with open(output_filename, "wb") as f:
                f.write(image_bytes)
            print(f"Image successfully generated and saved as '{output_filename}'")
        else:
            print("Error: No base64 image data found in the response.")
    else:
        print("Error: No predictions found in the API response.")
        print(f"Full response: {result}")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {http_err.response.text}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An unexpected request error occurred: {req_err}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")