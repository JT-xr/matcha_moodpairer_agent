#test_cafe.py
from cafe_search import search_matcha_cafes

cafes = search_matcha_cafes("Brooklyn, NY")
for c in cafes:
    print(f"{c['name']} - {c['address']} ({c['rating']}⭐)\n{c['map_link']}\n")