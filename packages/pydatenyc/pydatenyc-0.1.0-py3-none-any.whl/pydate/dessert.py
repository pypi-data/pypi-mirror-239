import json
import random
import os

def dessert(type, price):
  script_dir = os.path.dirname(os.path.abspath(__file__))
  json_path = os.path.join(script_dir, '../data/desserts.json')
  with open(json_path, "r") as file:
    shops = json.load(file)

  found_shops = []
  for shop in shops:
    type_match = type == shop["type"]
    price_match = price == shop["price"]   
    if type_match and price_match:
      found_shops.append(shop)

  if found_shops:
    recommended_dessert = random.choice(found_shops)
    recommended_dessert = f"Dessert Shop: {recommended_dessert['name']}\nType: {recommended_dessert['type']}\nPrice: {recommended_dessert['price']}"
  else:
    recommended_dessert = "Oops, no desserts found"
  return recommended_dessert
  