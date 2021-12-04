import operator
from models import Wine

WINES = [
    {'name': 'red', 'score': 10}, 
    {'name': 'sparkling', 'score': 3}, 
    {'name': 'white', 'score': 2}, 
    {'name': 'rosé', 'score': 6}, 
    {'name': 'fortified', 'score': 0}
]


WINES.sort(key=operator.itemgetter('score'), reverse=True)

preferences = {
    "is_vegan" : 0,
    "non_alcoholic_wines": 1,
    "alcoholic_wines": 1,
    "price_range": (1, 70000)
}


#     0{ "name": "red", "score": 0 },
#     1{ "name": "sparkling", "score": 0 },
#     2{ "name": "white", "score": 0 },
#     3{ "name": "rosé", "score": 0 },
#     4{ "name": "fortified", "score": 0 },

# {'name': 'Lambrusco', 'type': 'red', 'price': 20, 'is_alcoholic': 1, 'is_vegan': 1}
