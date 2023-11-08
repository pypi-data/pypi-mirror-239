import json
import random
import os

def pickupline(text=False, category=None):
    if(not isinstance(text, bool)):
        return "The text flag must be a boolean. Try again."
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, '../data/pickuplines.json')
    with open(json_path, "r") as file:
        lines = json.load(file)

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
