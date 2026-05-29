from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://menahabhandari:{password}@cluster1.kj57mcg.mongodb.net/?appName=Cluster1"
client = MongoClient(connection_string)

dbs = client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()
def insert_test_doc():
    collection = test_db.test
    test_document = {
        "name": "rina",
        "type": "test"
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)
production = client.production
person_collection = production.person_collection
def create_documents():
    first_name = ["rina", "tim", "ram"]
    last_name = ["gupta", "goyal", "sharma"]
    age = [ 19, 20, 21]
    docs = []

    for first_name, last_name, age in zip(first_name, last_name, age):
        doc = {"first_name": first_name, "last_name": last_name, "age":age}
        docs.append(doc)
    person_collection.insert_many(docs)
printer = pprint.PrettyPrinter()



def find_all_people():
    people = person_collection.find()
    for person in people: 
        printer.pprint(person)


def find_rina():
    rina = person_collection.find_one({"first_name": "rina"})
    printer.pprint(rina)


def count_all_people():
    count = person_collection.count_documents(filter={})
    print("number of people", count)


def get_person_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id":_id})
    printer.pprint(person)


def get_age_range(min_age, max_age):
    query =  {"$and": [
            {"age": {"$gte": min_age}},
            {"age": {"$lte": max_age}}
        ]}
    
    people = person_collection.find(query).sort("age")
    for person in people:
        printer.pprint(person)


def project_colums():
    columns = {"_id": 0, "first_name": 1, "last_name": 1}
    people = person_collection.find({}, columns)
    for person in people:
        printer.pprint(person)

def update_person_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)

    #all_updates = {
        #"$set": {"new_field": True},
        #"$inc": {"age": 1},
        #"$rename": {"first_name": "first", "last_name": "last"}
    #}
    #person_collection.update_one({"_id": _id}, all_updates)
    person_collection.update_one({"_id": _id}, {"$unset": {"new_field": ""}})

def replace_one(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    new_doc = {
        "first_name": "new first name",
        "last_name": "new last name",
        "age": 30
    }

    person_collection.replace_one({"_id":_id}, new_doc)


def delete_doc_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    person_collection.delete_one({"_id": _id})


address = {
"_id":"62475964011a9126a4cebeb7",
"street":"Bay Street",
"number":2706,
"city": "San Francisco",
"country":"United States",
"zip": "94107"
}

def add_address_embed(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    person_collection.update_one({"_id":_id}, {"$addToSet":{"addresses": address}})


def add_address_relationship(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    address = address.copy()
    address["owner_id"] = person_id
    
    address_collection = production.address
    address_collection.insert_one(address)
def names_having_a():
    names_containing_a = person_collection.find({"first_name": {"$regex": "a{1}"}})
    printer.pprint(list(names_containing_a))












