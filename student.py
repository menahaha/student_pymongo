from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://menahabhandari:{password}@cluster1.kj57mcg.mongodb.net/?appName=Cluster1"
client = MongoClient(connection_string)
dbs = client.list_database_names()
production = client.production
student_collection = production.student_collection
users_collection = production.users

def create_documents():
    first_names = ["rina", "tim", "ram"]
    last_names = ["gupta", "goyal", "sharma"]
    ages = [19, 20, 21]
    cgpas = [8.5, 7.8, 9.1]
    docs = []
    for first_name, last_name, age, cgpa in zip(first_names, last_names, ages, cgpas):
        doc = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "cgpa": cgpa,
        
        }
        docs.append(doc)
    student_collection.insert_many(docs)

printer = pprint.PrettyPrinter()

def add_student(first_name, last_name, age, cgpa):
    student = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "cgpa": cgpa
    }
    new_student = student_collection.insert_one(student)

    print("Inserted ID:", new_student.inserted_id)


def find_all_students():
    students = list(student_collection.find())
    for student in students:
        student["_id"] = str(student["_id"])
    return students

def find_rina():
    rina = student_collection.find_one({"first_name": "rina"})
    printer.pprint(rina)

def count_all_students():
    count = student_collection.count_documents(filter={})
    print("number of students:", count)

def get_student_by_id(student_id):
    from bson.objectid import ObjectId

    _id = ObjectId(student_id)

    student = student_collection.find_one({"_id": _id})
    student["_id"] = str(student["_id"])
    return student

def get_age_range(min_age, max_age):
    query = {
        "$and": [
            {"age": {"$gte": min_age}},
            {"age": {"$lte": max_age}}
        ]
    }
    students = student_collection.find(query).sort("age")
    for student in students:
        printer.pprint(student)

def get_cgpa_range(min_cgpa, max_cgpa):
    query = {
        "$and": [
            {"cgpa": {"$gte": min_cgpa}},
            {"cgpa": {"$lte": max_cgpa}}
        ]
    }
    students = student_collection.find(query).sort("cgpa")

    for student in students:
        printer.pprint(student)

def project_columns():
    columns = {
        "_id": 0,
        "first_name": 1,
        "last_name": 1,
        "cgpa": 1
    }

    students = student_collection.find({}, columns)

    for student in students:
        printer.pprint(student)

def update_student_by_id(student_id, dept, cgpa_inc):
    from bson.objectid import ObjectId

    _id = ObjectId(student_id)

    all_updates = {
        "$set": {"dept": dept},
        "$inc": {"cgpa": cgpa_inc}
        
    }

    student_collection.update_one({"_id": _id}, all_updates)


def replace_one(student_id):
    from bson.objectid import ObjectId

    _id = ObjectId(student_id)

    new_doc = {
        "first_name": "new",
        "last_name": "student",
        "age": 22,
        "cgpa": 8.0
    }

    student_collection.replace_one({"_id": _id}, new_doc)


def delete_doc_by_id(student_id):
    from bson.objectid import ObjectId

    _id = ObjectId(student_id)

    student_collection.delete_one({"_id": _id})


school_address = {
    "_id": "6a1958bbd15341bbcde6acf9",
    "school_name": "Delhi Public School",
    "street": "Park Road",
    "number": 101,
    "city": "Delhi",
    "country": "India",
    "zip": "110001"
}

def add_school_address_embed(student_id, school_address):
    from bson.objectid import ObjectId

    _id = ObjectId(student_id)

    student_collection.update_one(
        {"_id": _id},
        {"$addToSet": {"school_address": school_address}}
    )

def add_school_address_relationship(student_id, school_address):
    from bson.objectid import ObjectId

    _id = ObjectId(student_id)

    school_address = school_address.copy()
    school_address["student_id"] = _id

    address_collection = production.school_address
    address_collection.insert_one(school_address)


def names_having_a():
    names_containing_a = student_collection.find({"first_name": {"$regex": "a{1}"}})
    printer.pprint(list(names_containing_a))

def get_cgpa_avg():
    result = student_collection.aggregate([
        {
            "$group":
            {"_id": None , "avgcgpa": {"$avg": "$cgpa"} }
        }
    ])
    for data in result:
        return data
def join_student_to_address():
    result = student_collection.aggregate([{
        "$lookup": {
            "from" : "school_address",
            "localField": "_id",
            "foreignField": "student_id",
            "as": "address"
        }
    }])
    printer.pprint(list(result))

def get_time_created(student_id):
    from bson.objectid import ObjectId
    _id = ObjectId(student_id)
    print(_id.generation_time)

def get_ist(student_id):
    from zoneinfo import ZoneInfo
    from bson.objectid import ObjectId
    _id = ObjectId(student_id)
    ist_time = _id.generation_time.astimezone(
        ZoneInfo("Asia/Kolkata")
    )
    print(ist_time)

users_collection.update_one(
    {"username": "harish"},
    {"$set": {"role": "admin"}}
)


