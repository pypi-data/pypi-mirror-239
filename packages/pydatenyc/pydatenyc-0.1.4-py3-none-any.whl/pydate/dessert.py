import json
import random
import os
import pkg_resources

shops1 = [
    {
      "name": "Culture: An American Yogurt Co",
      "price": "medium",
      "type": "frozen"
    },
    {
      "name": "Ralphs Famous Italian Ices & Ice Cream",
      "price": "low",
      "type": "frozen"
    },
    {
      "name": "Chinatown Ice Cream Factory",
      "price": "low",
      "type": "frozen"
    },
    {
      "name": "Van Leeuwen",
      "price": "medium",
      "type": "frozen"
    },
    {
      "name": "Venchi",
      "price": "high",
      "type": "frozen"
    },
    {
      "name": "Amorino",
      "price": "high",
      "type": "frozen"
    },

    {
      "name": "Insomnia Cookies",
      "price": "low",
      "type": "bakery"
    },
    {
      "name": "Paris Baguette",
      "price": "medium",
      "type": "bakery"
    },
    {
      "name": "Breads Bakery",
      "price": "medium",
      "type": "bakery"
    },
    {
      "name": "Levain Bakery",
      "price": "medium",
      "type": "bakery"
    },
    {
      "name": "Dominique Ansel Bakery",
      "price": "high",
      "type": "bakery"
    },
    {
      "name": "Lady M Confections",
      "price": "high",
      "type": "bakery"
    },
    
    {
      "name": "See's Candies",
      "price": "low",
      "type": "candy"
    },
    {
      "name": "Economy Candy",
      "price": "low",
      "type": "candy"
    },
    {
      "name": "M&M's New York",
      "price": "low",
      "type": "candy"
    },
    {
      "name": "Dylan's Candy Bar",
      "price": "medium",
      "type": "candy"
    },
    {
      "name": "Lindt Chocolate Shop",
      "price": "medium",
      "type": "candy"
    },
    {
      "name": "BonBon - A Swedish Candy Co",
      "price": "medium",
      "type": "candy"
    },
    {
      "name": "Sugarfina",
      "price": "high",
      "type": "candy"
    },
    {
      "name": "ROYCE' Chocolate",
      "price": "high",
      "type": "candy"
    }
]

def dessert(type="candy", price="low"):
  try:
    json_path = pkg_resources.resource_filename(__name__, 'data/desserts.json')
    with open(json_path, "r") as file:
      shops = json.load(file)
  except Exception as e:
    shops = shops1


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
  