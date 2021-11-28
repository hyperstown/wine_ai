import re
from datetime import datetime
#from models import Wine

WINES = [
    { "name": "red", "score": 0 },
    { "name": "sparkling white", "score": 0 },
    { "name": "white", "score": 0 },
    { "name": "sparkling rosé", "score": 0 },
    { "name": "fortified", "score": 0 },
]

AUTO_TIME_DETECT = False

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


def re_input(question):
    """ Returns True if answer matches 'yes' else returns False """
    answer = input(question)
    return bool(re.search("[JjSsYy]+", answer))

def user_interview():

    # Control questions

    is_adult = re_input("Are you an adult? [Y/n] ")
    non_alcoholic_wines = re_input("Are you interested in non alcoholic wines [Y/n] ")
    if not is_adult and not non_alcoholic_wines:
        return {} # exits program
    
    is_drunk = re_input("Are you drunk?  [Y/n] ")

    if is_drunk and not non_alcoholic_wines:
        return {}
    
    is_vegan = re_input("Are you a vegan?  [Y/n] ")

    # Favorite type

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
        if favorite_wine_int in available_choices:
            WINES[favorite_wine_int - 1]["score"] += 4


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
            time_of_day = input("Select:")
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

    if daytime == "Morning":
        WINES[2]["score"] += 2
        WINES[1]["score"] += 2
        if favorite_wine_int == 1:
            WINES[0]["score"] += 1
    elif daytime == "Noon":
        WINES[3]["score"] += 2
        WINES[1]["score"] += 1
    elif daytime == "Afternoon":
        WINES[3]["score"] += 2
        WINES[1]["score"] += 1
                

    print(WINES)

def main():
    user_interview()


#     0{ "name": "red", "score": 0 },
#     1{ "name": "sparkling white", "score": 0 },
#     2{ "name": "white", "score": 0 },
#     3{ "name": "sparkling rosé", "score": 0 },
#     4{ "name": "fortified", "score": 0 },


# Afternoon:
# fortified         - 2 points
# white            - 1 point



if __name__ == '__main__':
    main()

# {'name': 'Lambrusco', 'type': 'red', 'price': 20, 'is_alcoholic': 1, 'is_vegan': 1}
