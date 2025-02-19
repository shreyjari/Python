from tinydb import TinyDB, Query
db = TinyDB('db.json')

user = Query()

def insert():
    db.insert({'name': 'Shrey', 'age': 23, 'city': 'Mumbai'})
    db.insert({'name': 'Josh', 'age': 21, 'state': 'Gujarat'})
    db.insert({'name': 'Jay', 'age': 22})
    db.insert({'name': 'Sarah', 'age': 25})
    db.insert({'name': 'Max', 'age': 24})

def search():
    results = db.search(user.age > 23)
    #print(results)

def update():
    db.update({'age': 2456}, user.name == 'Shrey')

#insert()
#search()
update()
print(db.all())