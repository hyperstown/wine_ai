import re
from datetime import datetime
from .settings import *
from remote_debugger.debug_client import send_debug

WINES = [
    { "name": "red", "score": 0 },
    { "name": "sparkling", "score": 0 },
    { "name": "white", "score": 0 },
    { "name": "rosé", "score": 0 },
    { "name": "fortified", "score": 0 },
]

_WINES_MAP = {
    "red" : 0,
    "sparkling" : 1,
    "white" : 2,
    "rosé" : 3,
    "fortified" : 4,
}

def print_debug(*values):
    if DEBUG and REMOTE_DEBUGGING:
        send_debug(values)
    elif DEBUG:
        print("[DEBUG]", *values)

def increment_score(wine, score_increment=1):
    """ Increment wine score """
    if isinstance(wine, int):
        WINES[wine]["score"] += score_increment
    else:
        WINES[_WINES_MAP[wine]]["score"] += score_increment

def detect_time_of_the_day():
    hour = datetime.now().hour
    if (hour > 6) and (hour <= 12):
        return 'Morning'
    elif (hour > 12) and (hour <= 16):
        return 'Noon'
    elif (hour > 16) and (hour <= 20) :
        return 'Afternoon'
    elif (hour > 20) and (hour <= 6):
        return 'Evening' # technically night xd


def re_input(prompt):
    """ Returns True if answer matches 'yes' else returns False """
    answer = input(prompt)
    return bool(re.search("[JjSsYy]+|^$", answer))

def safe_age_input(prompt="Please specify your age: "):
    while True:
        try:
            user_age = int(input(prompt))
            if user_age <= 0:
                raise ValueError()
        except ValueError:
            print("Incorrect value!")
        else:
            break
    return user_age

def get_price_range(price_range):
    range_list = price_range.split('-')
    if len(range_list) != 2:
        return () # empty tuple

    try:
        min_price = int(range_list[0])
        max_price = int(range_list[1])
    except ValueError:
        return () # could not convet to int
    else:
        return (min_price, max_price)


# helpers - for now no need to put it in separate file.

def drunk_preferences(alcoholic_wines, non_alcoholic_wines):
    """
    alcoholic_wines=True, non_alcoholic_wines=False # returns True
    alcoholic_wines=False, non_alcoholic_wines=True # returns False

    1 with 0 # true
    0 with 1 # false
    """
    return bool((alcoholic_wines - non_alcoholic_wines) + 1)

def get_fav_wine_type():
    print("What is your favorite wine type?")
    print("Choices")
    available_choices = []
    for choice, wine in enumerate(WINES):
        available_choices.append(choice + 1)
        print(choice + 1, " - ", wine.get('name'))
    print("Anything else - No preference")
    favorite_wine = input("Select: ")
    try:
        favorite_wine_int = int(favorite_wine)
    except ValueError:
        favorite_wine_int = -1
    else:
        if not favorite_wine_int in available_choices:
            favorite_wine_int = -1

    return favorite_wine_int


def get_time_of_the_day():
    # Time of the day
    if AUTO_TIME_DETECT:
        daytime = detect_time_of_the_day()
    else:
        while True:
            print("Select time of the day")
            print("Choices:")
            print("1 - Morning")
            print("2 - Noon")
            print("3 - Afternoon")
            print("4 - Evening")
            time_of_day = input("Select: ")
            if time_of_day == "1":
                daytime = "Morning"
                break
            elif time_of_day == "2":
                daytime = "Noon"
                break
            elif time_of_day == "3":
                daytime = "Afternoon"
                break
            elif time_of_day == "4":
                daytime = "Evening"
                break
            else:
                print("Incorrect choice")

    return daytime

def get_meeting_type():
    while True:
        print("Select type of meeting")
        print("Choices:")
        print("1 - Business")
        print("2 - Relatives")
        print("3 - Friends")
        print("4 - Picnic")
        print("5 - Drinks")
        type_of_meeting = input("Select: ")
        if type_of_meeting in ["1","2","3","4","5"]:
            break
        else:
            print("Incorrect choice")

    return type_of_meeting


def get_dish_type():
    while True:
        print("Select type of dish")
        print("Choices:")
        print("1 - Red meat")
        print("2 - Poultry")
        print("3 - Pasta")
        print("4 - Fish")
        print("5 - Pork")
        print("6 - Barbecue")
        print("7 - Seafood")
        print("8 - Salad")
        print("9 - Dessert")
        print("10 - Appetizer and snacks")
        type_of_dish = input("Select: ")
        if type_of_dish in ["1","2","3","4","5","6","7","8","9","10"]:
            break
        else:
            print("Incorrect choice")

    return type_of_dish


