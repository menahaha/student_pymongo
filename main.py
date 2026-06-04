from fastapi import FastAPI
from pydantic import BaseModel
from student import *
from auth import *
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer( tokenUrl= "login")

def get_current_user( token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

def admin_only(user = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail= "admins only")
    return user

@app.get("/")
def home():
    return{"message": "home"}

@app.get("/all_students")
def get_students(user = Depends(get_current_user)):
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
def update_student(student_id: str, student: Update_Student, user = Depends(get_current_user)):
    return update_student_by_id(student_id, student.dept, student.cgpa_inc)

@app.delete("/students/{student_id}")
def delete_student(student_id: str, user=Depends(admin_only)):
    return delete_doc_by_id(student_id)

@app.get("/avgcgpa")
def avg_cgpa():
    return get_cgpa_avg()

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
        hashed = hash_password(user.password)

        users_collection.insert_one({
            "username": user.username,
            "password": hashed,
            "role": "user"
        })
        return {"message": "user registered"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = users_collection.find_one({
        "username": form_data.username
    })
    if not db_user:
        return {"message": "user not found"}
    if not verify_password(form_data.password, db_user["password"]):
        return {"message": "incorrect password"}
    token = create_access_token({
        "username": db_user["username"],
        "role": db_user["role"]
    })
    return {
        "access_token": token,
        "token_type": "bearer"
    }


   
