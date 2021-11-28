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
        WINES[4]["score"] += 2
        WINES[2]["score"] += 1
    elif daytime == "Evening":
        WINES[0]["score"] += 2
        WINES[3]["score"] += 1
                

    # Price range
    while True:
        print("Specify your price range in format 'dd-dd' for example '100-500'")
        print("If you don't care just hit enter")
        price_range =  input("Range: ")
        if not price_range:
            price_range_tuple = ()
            break

        price_range_tuple = get_price_range(price_range)
        if not price_range_tuple:
            print("Incorrect price range:", price_range)

    
    # Type of meeting

    while True:
        print("Select type of meeting")
        print("Choices:")
        print("1 - Business")
        print("2 - Relatives")
        print("3 - Friends")
        print("4 - Picnic")
        print("5 - Drinks")
        type_of_meeting = input("Select:")
        if type_of_meeting == "1":
            WINES[0]["score"] += 2
            break
        elif type_of_meeting == "2":
            WINES[2]["score"] += 2
            break
        elif type_of_meeting == "3":
            WINES[1]["score"] += 2
            break
        elif type_of_meeting == "4":
            WINES[3]["score"] += 2
            break
        elif type_of_meeting == "5":
            WINES[4]["score"] += 2
            break
        else:
            print("Incorrect choice")
    

    # User age

    while True:
        user_age_raw = input("Enter your age: ")
        try:
            user_age = int(user_age_raw)
        except ValueError:
            print("Incorrect value!")
        else:
            if user_age < 18:
                print("You lied about being an adult earlier!")
                return {}
            break
    
    if user_age in range(18, 34):
        WINES[1]["score"] += 1
        WINES[3]["score"] += 1
    elif user_age in range(35, 54):
        WINES[0]["score"] += 1
    else:
        WINES[2]["score"] += 1
        WINES[4]["score"] += 1

    print(WINES)

def main():
    user_interview()

# Business    - red            - 2 points
# Relatives    - white            - 2 points
# Friends    - sparkling white    - 2 points
# Picnic        - sparkling rosé    - 2 points
# Drinks        - fortified        - 2 points


#     0{ "name": "red", "score": 0 },
#     1{ "name": "sparkling white", "score": 0 },
#     2{ "name": "white", "score": 0 },
#     3{ "name": "sparkling rosé", "score": 0 },
#     4{ "name": "fortified", "score": 0 },



if __name__ == '__main__':
    main()

# {'name': 'Lambrusco', 'type': 'red', 'price': 20, 'is_alcoholic': 1, 'is_vegan': 1}
