from fastapi import FastAPI
from pydantic import BaseModel

# Entity user
class User(BaseModel):
    id: int
    name: str
    email: str
    password: str

user_list = [
    User(id=1, name="John Doe", email="john.doe@example.com", password="securepassword"),
    User(id=2, name="Jane Smith", email="jane.smith@example.com", password="anotherpassword"),
    User(id=3, name="Alice Johnson", email="alice.johnson@example.com", password="thirdpassword"),
]

app = FastAPI()
@app.get("/users")
async def users():
    return user_list

@app.get("/user/{id}")
async def user(id: int):
    return search_user_by_id(id)

@app.post("/user")
async def create_user(user: User):
    if check_user_exists(user.id):
        return {"error": "User with this ID already exists"}
    if check_user_exists_by_email(user.email):
        return {"error": "User with this email already exists"}
    user_list.append(user)
    return user

@app.put("/user/{id}")
async def update_user(id: int, updated_user: User):
    for index, user in enumerate(user_list):
        if user.id == id:
            if updated_user.email != user.email and check_user_exists_by_email(updated_user.email):
                return {"error": "User with this email already exists"}
            user_list[index] = updated_user
            return updated_user
    return {"error": "User not found"}

@app.delete("/user/{id}")
async def delete_user(id: int):
    for index, user in enumerate(user_list):
        if user.id == id:
            del user_list[index]
            return {"message": "User deleted successfully"}
    return {"error": "User not found"}

def search_user_by_id(id: int):
    for user in user_list:
        if user.id == id:
            return user
    return {"error": "User not found"}

def check_user_exists(id: int):
    if(type(search_user_by_id(id)) == User):
        return True
    return False

def check_user_exists_by_email(email: str):
    for user in user_list:
        if user.email == email:
            return True
    return False