import csv
from core.migrations import migrate
from models import Wine


def convert_csv(dict_list):
    result = []
    for i in dict_list:
        i['is_vegan'] = int(i['is_vegan'])
        i['is_alcoholic'] = int(i['is_alcoholic'])
        i['price'] = int(i['price'])
        result.append(i)
    return result

def main():
    migrate()
    with open('wine_db.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dl = convert_csv(reader)
        for r in dl:
            #print(r)
            new_wine = Wine(**r)
            new_wine.save()
        print("Done!")




if __name__ == '__main__':
    main()

# {'name': 'Lambrusco', 'type': 'red', 'price': 20, 'is_alcoholic': 1, 'is_vegan': 1}
