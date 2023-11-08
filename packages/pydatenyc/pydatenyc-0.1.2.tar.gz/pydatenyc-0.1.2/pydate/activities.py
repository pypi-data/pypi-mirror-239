import json
import random
import os
import six
import pkg_resources


def activity(indoor=True, time="evening"):
    if(not isinstance(time, six.string_types) or not type(indoor)==bool):
        return "Your filter is invalid. Try again."
    
    json_path = pkg_resources.resource_filename(__name__, 'data/activities.json')
    with open(json_path, "r") as file:
        activities = json.load(file)

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