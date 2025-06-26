# test_gemini.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Suggest a creative matcha drink for a cozy mood. Don't list any ingredients or instructions just the name of the drink. However, you can also include a 20 word description drink while mentioning 1-3 the ingridents plus how the drink will make you feel cozy written in a creative way.")
print(response.text)