from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import uuid

app = FastAPI()

@app.get("/")
def read_root():
    return {"JUSTPAY"}

class Gender(str, Enum):
    male = "male"
    female = "female"

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"

class Region(str, Enum):
    Europe = "Europe"
    America = "America"

class AccountType(str, Enum):
    principal = 1
    secondary = 0

class User(BaseModel):
    id : str =  uuid.uuid4()
    pseudo: str 
    name: str
    firstname: str
    password: str
    email: str
    age: int
    region: str
    gender: str

class BankAccount(BaseModel):
    name: str
    firstname: str
    email: str
    age: int
    account_number: str
    balance: float = 0.0
    account_type: str
    currency: str = "EUR"
    user_id: int

class Beneficiary(BaseModel):
    name: str
    account_number: str 
    

def create_user(pseudo: str, name: str, firstname: str, password: float, email: str, age: int, region: Region, gender: Gender):    
    
    User = User(pseudo=pseudo, name=name, firstname=firstname, password=password, email=email, age=age, region=region, gender=gender)
    create_bank_account(name=name, firstname=firstname, email=email, age=age, account_number=str(uuid.uuid4()), account_type=AccountType.principal, user_id=User.id)
    return {"message": "User created", "user": User.name}

def get_user(user_id: int):
    return {"message": "User details", "user_id": user_id}
def update_user(user_id: int, user: User):    return {"message": "User updated", "user_id": user_id, "user": user}
def delete_user(user_id: int): return {"message": "User deleted", "user_id": user_id}
    
def create_bank_account(user : User):    return {"message": "Bank account created", "account": user}
def get_bank_account(account_id: int):    return {"message": "Bank account details", "account_id": account_id}
def update_bank_account(account_id  : int, account: BankAccount):    return {"message": "Bank account updated", "account_id": account_id, "account": account}
def delete_bank_account(account_id: int):    return {"message": "Bank account deleted", "account_id": account_id}


    