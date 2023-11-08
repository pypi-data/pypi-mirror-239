import json
import random
import os
import six
import pkg_resources

activities1 = [
    {
        "activity": "Hiking",
        "indoor": False,
        "time": "morning"
    },
    {
        "activity": "pizza dinner",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "sushi dinner",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Star-gazing",
        "indoor": False,
        "time": "evening"
    },
    {
        "activity": "Beach Picnic",
        "indoor": False,
        "time": "afternoon"
    },
    {
        "activity": "Cooking Class",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Art Gallery Visit",
        "indoor": True,
        "time": "afternoon"
    },
    {
        "activity": "Movie Night",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Botanical Garden Tour",
        "indoor": False,
        "time": "morning"
    },
    {
        "activity": "Ice Skating",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Wine Tasting",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Zoo Visit",
        "indoor": False,
        "time": "afternoon"
    },
    {
        "activity": "Live Music Concert",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Biking in the Park",
        "indoor": False,
        "time": "morning"
    },
    {
        "activity": "Sunset Beach Walk",
        "indoor": False,
        "time": "evening"
    },
    {
        "activity": "Dinner and a Movie",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Visit an Escape Room",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Wine and Paint Night",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Visit a Farmer's Market",
        "indoor": False,
        "time": "morning"
    },
    {
        "activity": "Museum Exploration",
        "indoor": True,
        "time": "afternoon"
    },
    {
        "activity": "Coffee and Dessert Date",
        "indoor": True,
        "time": "evening"
    },
    {
        "activity": "Nature Hike and Picnic",
        "indoor": False,
        "time": "morning"
    }
]

def activity(indoor=True, time="evening"):
    if(not isinstance(time, six.string_types) or not type(indoor)==bool):
        return "Your filter is invalid. Try again."
    try:
        json_path = pkg_resources.resource_filename(__name__, 'data/activities.json')
        with open(json_path, "r") as file:
            activities = json.load(file)
    except Exception as e:
        activities = activities1

    filtered_activities = []
    for activity in activities:
        indoor_match = indoor == activity["indoor"]
        time_match = time.lower() == activity["time"].lower()      
        if indoor_match and time_match:
            filtered_activities.append(activity)

    if filtered_activities:
        recommended_activity = random.choice(filtered_activities)
        recommended_activity = f"Activity: {recommended_activity['activity']}\nindoor: {'yes' if recommended_activity['indoor'] else 'no'}\ntime: {recommended_activity['time']}"
    else:
        recommended_activity = "Stay home and relax."
    return recommended_activity