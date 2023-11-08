import json
import random
import os
import pkg_resources

lines1 = [
    {
      "pick_up_line": "You're like my favorite book, I can't put you down.",
      "suitable_for_text": False,
      "categories": ["Literary", "Compliment"]
    },
    {
      "pick_up_line": "Guess what I’m wearing? The smile you just gave me. 😊",
      "suitable_for_text": True,
      "categories": ["Compliment", "Sweet", "Cute"]
    },
    {
      "pick_up_line": "Do you have a map? I just got lost in your eyes.",
      "suitable_for_text": False,
      "categories": ["Romantic", "Classic"]
    },
    {
      "pick_up_line": "U must be tired coz u've been running in my mind all day. 😴",
      "suitable_for_text": True,
      "categories": ["Classic", "Cute"]
    },
    {
      "pick_up_line": "Let's make a deal? I'll give you a kiss and if you don't like it, you can return it.",
      "suitable_for_text": False,
      "categories": ["Bold", "Direct"]
    },
    {
      "pick_up_line": "Do you have a name, or can I call you mine? 📞",
      "suitable_for_text": True,
      "categories": ["Cute", "Direct"]
    },
    {
      "pick_up_line": "Are you a 90-degree angle? Because you are looking right.",
      "suitable_for_text": False,
      "categories": ["Geeky", "Clever"]
    },
    {
      "pick_up_line": "Is it hot in here or is it just our DM convo? 🔥",
      "suitable_for_text": True,
      "categories": ["Suggestive", "Modern"]
    },
    {
      "pick_up_line": "You must be a high test score. Because I want to take you home and show you to my mother.",
      "suitable_for_text": False,
      "categories": ["Clever", "Compliment", "Funny"]
    },
    {
      "pick_up_line": "R u a camera? Because every time I look at you, I smile. 📸",
      "suitable_for_text": True,
      "categories": ["Whimsical", "Sweet"]
    },
    {
      "pick_up_line": "Are you my homework? 'Cause I'm not doing you but I definitely should be.",
      "suitable_for_text": False,
      "categories": ["Edgy", "Humorous", "Funny"]
    },
    {
      "pick_up_line": "Aside from being sexy, what do you do for a living? 💼",
      "suitable_for_text": True,
      "categories": ["Flirty", "Direct"]
    },
    {
      "pick_up_line": "I'm not a mathematician, but I'm pretty good with numbers. Tell you what, give me yours and watch what I can do with it.",
      "suitable_for_text": False,
      "categories": ["Confident", "Clever", "Funny"]
    },
    {
      "pick_up_line": "Are you Wi-Fi? Coz I'm feeling a connection. 📶",
      "suitable_for_text": True,
      "categories": ["Tech", "Modern"]
    },
    {
      "pick_up_line": "I was blinded by your beauty; I'm going to need your name and number for insurance purposes.",
      "suitable_for_text": False,
      "categories": ["Humorous", "Clever"]
    },
    {
      "pick_up_line": "If you were a vegetable, you’d be a ‘cute-cumber.’ 🥒",
      "suitable_for_text": True,
      "categories": ["Pun", "Cute"]
    },
    {
      "pick_up_line": "I'm learning about important dates in history. Wanna be one of them?",
      "suitable_for_text": False,
      "categories": ["Historical", "Clever"]
    },
    {
      "pick_up_line": "Send me your selfie so I can show Santa what I want for Christmas. 🎅",
      "suitable_for_text": True,
      "categories": ["Seasonal", "Cute", "Modern"]
    },
    {
      "pick_up_line": "Are you a time traveler? Because I see you in my future!",
      "suitable_for_text": False,
      "categories": ["Futuristic", "Romantic"]
    },
    {
      "pick_up_line": "You can't be my first, but you could be my next. 😘",
      "suitable_for_text": True,
      "categories": ["Direct", "Bold"]
    },
    {
      "pick_up_line": "Do you like Star Wars? Because Yoda only one for me!",
      "suitable_for_text": False,
      "categories": ["Nerdy", "Cute"]
    },
    {
    "pick_up_line": "Let's flip a coin. Head's your mine, tails I'm yours. 🪙",
    "suitable_for_text": True,
    "categories": ["Playful", "Cute"]
    },
    {
    "pick_up_line": "If you were a fruit, you'd be a fineapple",
    "suitable_for_text": False,
    "categories": ["Sweet", "Caring"]
    },
    {
    "pick_up_line": "Is your dad a boxer? Because you’re a knockout! 👊",
    "suitable_for_text": True,
    "categories": ["Compliment", "Clever"]
    },
    {
    "pick_up_line": "If I could rearrange the alphabet, I'd put U and I together.",
    "suitable_for_text": False,
    "categories": ["Classic", "Romantic"]
    },
    {
    "pick_up_line": "Do you have an Instagram? My mom said she wants to follow our relationship. 📷",
    "suitable_for_text": True,
    "categories": ["Modern", "Funny"]
    },
    {
    "pick_up_line": "Do you believe in love at first sight, or should I walk by again?",
    "suitable_for_text": False,
    "categories": ["Charming", "Classic"]
    },
    {
    "pick_up_line": "I’d say God Bless you, but it looks like he already did. 😇",
    "suitable_for_text": True,
    "categories": ["Blessed", "Compliment"]
    },
    {
    "pick_up_line": "You must be made of copper and tellurium because you’re CuTe.",
    "suitable_for_text": True,
    "categories": ["Science", "Clever"]
    },
    {
    "pick_up_line": "My parents always said I should follow my dreams. That's why I started following you on Instagram. 👀",
    "suitable_for_text": True,
    "categories": ["Contemporary", "Modern"]
    }
]


def pickupline(text=False, category=None):
    if(not isinstance(text, bool)):
        return "The text flag must be a boolean. Try again."
    
    try:
        json_path = pkg_resources.resource_filename(__name__, 'data/pickuplines.json')
        with open(json_path, "r") as file:
            lines = json.load(file)
    except Exception as e:
        lines = lines1


    filtered_lines = []
    for line in lines:  
        if line["suitable_for_text"] == text:
            if category is not None:
                for cat in line["categories"]:
                    if cat.lower() == category.lower():
                        filtered_lines.append(line)
            else:
                filtered_lines.append(line)


    if filtered_lines:
        line_object = random.choice(filtered_lines)
        line = line_object["pick_up_line"]
        recommended_line=f"Here's Your Pick Up Line, Use Wisely and With Caution: \n{line}"
    else:
        recommended_line = "I'm sorry. We didn't find any pick up lines matching your criteria. Try changing the category or text type."
    return recommended_line
