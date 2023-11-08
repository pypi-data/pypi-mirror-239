import json
import random
import os
import six
import pkg_resources

foods1 = [
    {
        "name": "Foie gras",
        "cuisine": "French",
        "price_range": "high",
        "meal": "dinner"
    },
    {
        "name": "Chicken and Mushroom Fricassee",
        "cuisine": "French",
        "price_range": "low",
        "meal": "dinner"
    },
    {
        "name": "Marseille-Style Shrimp Stew",
        "cuisine": "French",
        "price_range": "medium",
        "meal": "dinner"
    },
    {
        "name": "Short Rib Bourguignon",
        "cuisine": "French",
        "price_range": "medium",
        "meal": "dinner"
    },
    {
        "name": "Lobster Thermidor",
        "cuisine": "French",
        "price_range": "medium",
        "meal": "dinner"
    },
    {
        "name": "Dumplings",
        "cuisine": "Chinese",
        "price_range": "low",
        "meal": "lunch"
    },
    {
        "name": "Boiled Fish With Pickled Mustard",
        "cuisine": "Chinese",
        "price_range": "high",
        "meal": "lunch"
    }, 
    {
        "name": "Stinky Mandarin Fish",
        "cuisine": "Chinese",
        "price_range": "high",
        "meal": "lunch"
    }, 
    {
        "name": "Chinese Savior Crepe",
        "cuisine": "Chinese",
        "price_range": "low",
        "meal": "breakfast"
    }, 
    {
        "name": "Deep-fried Dough Sticks",
        "cuisine": "Chinese",
        "price_range": "low",
        "meal": "breakfast"
    }, 
    {
        "name": "Noodles with Soy Bean Paste",
        "cuisine": "Chinese",
        "price_range": "low",
        "meal": "lunch"
    },
    {
        "name": "Sautéed Bullfrog in Chili Sauce",
        "cuisine": "Chinese",
        "price_range": "high",
        "meal": "dinner"
    }
]

def food(cuisine="French", price_range="medium", meal="dinner"):
    if(not isinstance(cuisine, six.string_types) or not isinstance(price_range, six.string_types) or not isinstance(meal, six.string_types)):
        return "Your filter is invalid. Try again."
    
    try:
        json_path = pkg_resources.resource_filename(__name__, 'data/food.json')
        with open(json_path, "r") as file:
            foods = json.load(file)
    except Exception as e:
        foods = foods1


    filtered_foods = []
    for food in foods:
        cuisine_match = cuisine.lower() == food["cuisine"].lower()
        price_match = price_range.lower() == food["price_range"].lower()
        meal_match = meal.lower() == food["meal"].lower()      
        if cuisine_match and price_match and meal_match:
            filtered_foods.append(food)

    if filtered_foods:
        recommended_food = random.choice(filtered_foods)
        recommended_food=f"Recipe Name: {recommended_food['name']}\nCuisine: {recommended_food['cuisine']}\nPrice Range: {recommended_food['price_range']}\nMeal: {recommended_food['meal']}"
    else:
        recommended_food = "No food meets your requirements. Try again."
    return recommended_food
