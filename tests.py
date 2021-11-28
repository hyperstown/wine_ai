import operator

wines = [
    {'name': 'red', 'score': 10}, 
    {'name': 'sparkling white', 'score': 3}, 
    {'name': 'white', 'score': 2}, 
    {'name': 'sparkling rosé', 'score': 6}, 
    {'name': 'fortified', 'score': 0}
]


wines.sort(key=operator.itemgetter('score'), reverse=True)

print(wines[0])