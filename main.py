import sys
import operator

from experta import (
    Fact, KnowledgeEngine, Rule, OR, 
    AND, MATCH, P, NOT, DefFacts
)

from database.models import Wine
from database.init_db import init_now

from wine_ai.utils import *

class WineHelper(KnowledgeEngine):

    def get_best_wine(self):
        """ Fetches wine from database """
        preferences = self.preferences

        WINES.sort(key=operator.itemgetter('score'), reverse=True)
        wine_filter = {"type": WINES[0]["name"]}
        if preferences["is_vegan"]:
            wine_filter["is_vegan"] = preferences["is_vegan"]
        # if both are True no filter
        if preferences['alcoholic_wines'] ^ preferences['non_alcoholic_wines']:
            wine_filter['is_alcoholic'] = drunk_preferences(
                preferences['alcoholic_wines'], preferences['non_alcoholic_wines']
            )
        # if price range is specified filter that too.
        if preferences['price_range']:
            qs = Wine.objects.filter(**wine_filter).filter(
                Wine.price.between(preferences['price_range'][0], preferences['price_range'][1]), 
            ).order_by("price")
            if qs.count() == 0:
                qs = Wine.objects.filter(type=WINES[0]["name"]).order_by("price")
                if qs.count() == 0:
                    print("Something went wrong!")
                    # print(wine_filter)
                    return None
                show_all = re_input("No wine in current price range. Ignore limit? [Y/n] ")
                if not show_all:
                    return None   
        else:
            qs = Wine.objects.filter(**wine_filter).order_by("price")
    
        print("Recommended wine")
        wine = qs[-1]
        print("Name:", wine.name)
        print("Price:", wine.price, "PLN")
        print("Type:", wine.type)
        return None

    action = 1
    preferences = {
        "is_vegan" : False,
        "alcoholic_wines": False,
        "non_alcoholic_wines": False,
        "price_range": None
    }

    # here we define facts
    @DefFacts()
    def _initial_action(self):
        yield Fact(action='continue') # must be first
        yield Fact(user_age=safe_age_input())
        yield Fact(non_alcoholic_wines=re_input("Are you interested in non alcoholic wines [Y/n] "))
        yield Fact(alcoholic_wines=re_input("Are you interested in alcoholic wines [Y/n] "))
        yield Fact(is_drunk=re_input("Are you drunk?  [Y/n] "))
        yield Fact(is_vegan=re_input("Are you a vegan?  [Y/n] "))
        yield Fact(daytime=get_time_of_the_day())
        yield Fact(favorite_wine=get_fav_wine_type())
        yield Fact(type_of_meeting=get_meeting_type())
        yield Fact(type_of_dish=get_dish_type())

    @Rule(Fact(user_age=P(lambda x: x < 18)))
    def user_not_adult(self):
        print_debug("user_not_adult")
        self.declare(Fact(is_adult=False))        

    @Rule(Fact(user_age=P(lambda x: x > 18)))
    def user_adult(self):
        print_debug("user_adult")
        self.declare(Fact(is_adult=True))

    @Rule(Fact(user_age=P(lambda x: x >= 18) & P(lambda x: x <= 34)))
    def user_young(self):
        print_debug("user_young")
        increment_score('sparkling')
        increment_score('rosé')
    
    @Rule(Fact(user_age=P(lambda x: x >= 35) & P(lambda x: x <= 54)))
    def middle_age_young(self):
        print_debug("user_young")
        increment_score('red')

    @Rule(Fact(user_age=P(lambda x: x > 54)))
    def user_old(self):
        print_debug("user_old")
        increment_score('white')
        increment_score('fortified')

    @Rule(NOT(OR(Fact(is_adult=True), Fact(non_alcoholic_wines=True))))
    def user_not_qualified_age_perf(self):
        print_debug("user_not_qualified_age_perf")
        self.action = self.modify(
            self.facts[self.action], action='abort', reason='Selected non alcoholic wine but user underage! Exiting the program'
        ).__factid__

    @Rule(NOT(OR(Fact(alcoholic_wines=True), Fact(non_alcoholic_wines=True))))
    def impossible_criteria(self):
        print_debug("impossible_criteria")
        self.action = self.modify(
            self.facts[self.action], action='abort', reason='Selected non alcoholic and alcoholic wines. Critera are invalid. Abort.'
        ).__factid__

    @Rule(OR(Fact(is_drunk=True), Fact(non_alcoholic_wines=False)))
    def user_drunk(self):
        print_debug("user_drunk")
        self.action = self.modify(
            self.facts[self.action], action='abort', reason='Selected alcoholic wine but user drunk! Exiting the program'
        ).__factid__

    @Rule(Fact(is_vegan=True))
    def user_vegan(self):
        print_debug("user_vegan")
        self.preferences["is_vegan"] = True

    @Rule(Fact(alcoholic_wines=True))
    def alcoholic_wines_save_pref(self):
        print_debug("alcoholic_wines_save_pref")
        self.preferences["alcoholic_wines"] = True

    @Rule(Fact(non_alcoholic_wines=True))
    def non_alcoholic_wines_save_pref(self):
        print_debug("non_alcoholic_wines_save_pref")
        self.preferences["non_alcoholic_wines"] = True


    @Rule(Fact(favorite_wine=1))
    def fav_wine1(self):
        print_debug("fav_wine1 - red")
        increment_score("red", 4)

    @Rule(Fact(favorite_wine=2))
    def fav_wine2(self):
        print_debug("fav_wine2 - sparkling")
        increment_score("sparkling", 4)

    @Rule(Fact(favorite_wine=3))
    def fav_wine3(self):
        print_debug("fav_wine3 - white")
        increment_score("white", 4)

    @Rule(Fact(favorite_wine=4))
    def fav_wine4(self):
        print_debug("fav_wine4 - rosé")
        increment_score("rosé", 4)

    @Rule(Fact(favorite_wine=5))
    def fav_wine5(self):
        print_debug("fav_wine5 - fortified")
        increment_score("fortified", 4)


    @Rule(Fact(daytime="Morning"))
    def daytime_morning(self):
        print_debug("daytime - Morning")
        increment_score('white', 2) # += 2
        increment_score('sparkling', 2) # += 2

    @Rule(AND(Fact(daytime="Morning"), Fact(favorite_wine=1)))
    def daytime_morning_and_fav1(self):
        print_debug("daytime - Morning - and fav type 1")
        increment_score('red') # += 1

    @Rule(Fact(daytime="Noon"))
    def daytime_noon(self):
        print_debug("daytime - Noon")
        increment_score('rosé', 2) # += 2
        increment_score('sparkling') # += 1

    @Rule(Fact(daytime="Afternoon"))
    def daytime_afternoon(self):
        print_debug("daytime - Afternoon")
        increment_score('fortified', 2) # += 2
        increment_score('white') # += 1

    @Rule(Fact(daytime="Evening"))
    def daytime_evening(self):
        print_debug("daytime - Evening")
        increment_score('red', 2) # += 2
        increment_score('rosé') # += 1


    @Rule(Fact(type_of_meeting="1"))
    def meeting1(self):
        print_debug("Type of meeting 1")
        increment_score('red', 2) # += 2

    @Rule(Fact(type_of_meeting="2"))
    def meeting2(self):
        print_debug("Type of meeting 2")
        increment_score('white', 2) # += 2

    @Rule(Fact(type_of_meeting="3"))
    def meeting3(self):
        print_debug("Type of meeting 3")
        increment_score('sparkling', 2) # += 2

    @Rule(Fact(type_of_meeting="4"))
    def meeting4(self):
        print_debug("Type of meeting 4")
        increment_score('rosé', 2) # += 2

    @Rule(Fact(type_of_meeting="5"))
    def meeting5(self):
        print_debug("Type of meeting 5")
        increment_score('fortified', 2) # += 2

    
    @Rule(Fact(type_of_dish="1"))
    def dish1(self):
        print_debug("Type of dish 1")
        increment_score('red', 5) # += 5
        increment_score('rosé', 3) # += 3

    @Rule(Fact(type_of_dish="2"))
    def dish2(self):
        print_debug("Type of dish 2")
        increment_score('white', 4) # += 4
        increment_score('red', 2) # += 2

    @Rule(Fact(type_of_dish="3"))
    def dish3(self):
        print_debug("Type of dish 3")
        increment_score('white', 4) # += 4
        increment_score('red', 3) # += 3  

    @Rule(Fact(type_of_dish="4"))
    def dish4(self):
        print_debug("Type of dish 4")
        increment_score('white', 4) # += 4
        increment_score('sparkling', 3) # += 3

    @Rule(Fact(type_of_dish="5"))
    def dish5(self):
        print_debug("Type of dish 5")
        increment_score('sparkling', 4) # += 4
        increment_score('white', 3) # += 3

    @Rule(Fact(type_of_dish="6"))
    def dish6(self):
        print_debug("Type of dish 6")
        increment_score('red', 5) # += 5  

    @Rule(Fact(type_of_dish="7"))
    def dish7(self):
        print_debug("Type of dish 7")
        increment_score('sparkling', 4) # += 4
        increment_score('white', 3) # += 3
        increment_score('rosé', 2) # += 2
    
    @Rule(Fact(type_of_dish="8"))
    def dish8(self):
        print_debug("Type of dish 8")
        increment_score('white', 4) # += 4
        increment_score('sparkling', 3) # += 3

    @Rule(Fact(type_of_dish="9"))
    def dish9(self):
        print_debug("Type of dish 9")
        increment_score('fortified', 5) # += 5
        increment_score('rosé', 3) # += 3
        increment_score('sparkling', 3) # += 3

    @Rule(Fact(type_of_dish="10"))
    def dish10(self):
        print_debug("Type of dish 10")
        increment_score('fortified', 4) # += 4
        increment_score('white', 3) # += 3
        increment_score('rosé', 3) # += 3



    @Rule(Fact(action='abort', reason=MATCH.reason))
    def action_abort(self, reason):
        print_debug("abort")
        print("Program will not continue. Reason:", reason)

    @Rule(Fact(action='continue'))
    def fetch_wines(self):
        print_debug("continue")

        # Price range
        while True:
            print("Specify your price range in format 'dd-dd' for example '100-500'")
            print("If you don't care just hit enter")
            price_range =  input("Range: ")
            if not price_range:
                price_range_tuple = ()
                break

            price_range_tuple = get_price_range(price_range)
            if price_range_tuple:
                break
            print("Incorrect price range:", price_range)

        self.get_best_wine()


def main():
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    # args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if "--init" in opts or "--init-db" in opts:
        print_debug("Database initialized!")
        init_now()
    else:
        engine = WineHelper()
        try:
            engine.reset()
            engine.run()
        except KeyboardInterrupt:
            print("\nExiting...")


if __name__ == '__main__':
    main()
