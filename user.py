from enum import Enum
from bankAccount import create_primary_bank_account
from pydantic import BaseModel
import uuid
from pydantic import BaseModel, Field
from uuid import uuid4
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI, HTTPException

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    pseudo: str 
    name: str
    firstname: str
    hashed_password: str
    email: str
    age: int
    region: str
    gender: str


class Gender(str, Enum):
    male = "male"
    female = "female"


class Region(str, Enum):
    Europe = "Europe"
    America = "America"


class BaseModel(str, Enum):
    id: str = Field(default_factory=lambda: str(uuid4()))
    pseudo: str
    name: str
    firstname: str
    hashed_password: str
    email: str
    age: int
    region: Region
    gender: Gender

def create_user(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: Region, gender: Gender):    
    
    hashed_password = ph.hash(password)

    user = User(BaseModel)
    
    create_primary_bank_account(name=name, 
                        firstname=firstname, 
                        email=email, age=age, 
                        account_number=str(uuid.uuid4()), 
                        user_id=str(user.id))
    
    return user

def get_user(user_id: int, pseudo: str, name: str, firstname: str, email: str, age: int):
    
    User_dico = {"id": user_id, "pseudo": pseudo, "name": name, "firstname": firstname, "email": email, "age": age}
    return User_dico

def update_user(user_id: int, user: User):    
    return {"message": "User updated", "user_id": user_id, "user": user}

def delete_user(user_id: int): return {"message": "User deleted", "user_id": user_id}
    
def add_deposit(amount: int, balance: int):
    balance += amount
    return balance

ph = PasswordHasher()
def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False


app = FastAPI()

@app.post("/users")
def create_user_root(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: Region, gender: Gender):
    try:
        user = create_user(pseudo, name, firstname, password, email, age, region, gender)
        return {"message": "User created", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/users/{user_id}")
def get_user_root(user_id: int, pseudo: str, name: str, firstname: str, email: str, age: int):
    return get_user(user_id, pseudo, name, firstname, email, age)

@app.post("/users/deposit")
def add_deposit_root(amount: int, balance: int):
    new_balance = add_deposit(amount, balance)
    return {"new_balance": new_balance}
