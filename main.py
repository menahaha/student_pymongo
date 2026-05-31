from fastapi import FastAPI
from pydantic import BaseModel
from student import *
app = FastAPI()

@app.get("/")
def home():
    return{"message": "home"}

@app.get("/all_students")
def get_students():
    return find_all_students()

@app.get("/students/{student_id}")
def get_student(student_id: str):
    return get_student_by_id(student_id)

class Student(BaseModel):
    first_name: str
    last_name: str
    age: int
    cgpa : float

@app.post("/students")
def create_student(student:Student):
    return add_student(student.first_name, student.last_name, student.age, student.cgpa) 

class Update_Student(BaseModel):
    dept: str
    cgpa_inc: float


@app.put("/students/{student_id}")
def update_student(student_id: str, student: Update_Student):
    return update_student_by_id(student_id, student.dept, student.cgpa_inc)

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    return delete_doc_by_id(student_id)

@app.get("/avgcgpa")
def avg_cgpa():
    return get_cgpa_avg()