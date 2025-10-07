from enum import Enum
from bankAccount import create_primary_bank_account
from pydantic import BaseModel
import uuid
from pydantic import BaseModel

class User(BaseModel):
    id : str =  uuid.uuid4() #id: str = Field(default_factory=lambda: str(uuid4())) ID UNIQUE
    pseudo: str 
    name: str
    firstname: str
    password: str
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


def create_user(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: Region, gender: Gender):    
    
    user = User(pseudo=pseudo, 
                name=name, 
                firstname=firstname, 
                password=password, 
                email=email, 
                age=age, 
                region=region, 
                gender=gender)
    
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