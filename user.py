from enum import Enum

from sqlmodel import Session
from bankAccount import create_primary_bank_account
from pydantic import BaseModel
import uuid
from pydantic import BaseModel, Field
from uuid import uuid4
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI, HTTPException
from db.models import User

class Gender(str, Enum):
    male = "male"
    female = "female"


class Region(str, Enum):
    Europe = "Europe"
    America = "America"

def create_user(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: Region, gender: Gender, session:Session):    
    
    hashed_password = ph.hash(password)

    user = User(BaseModel)
    
    create_primary_bank_account(name=name, 
                        firstname=firstname, 
                        email=email, age=age, 
                        account_number=str(uuid.uuid4()), 
                        user_id=str(user.id))
    
    session.add(user)
    session.commit()
    
    return user

def get_user(user_id: int, pseudo: str, name: str, firstname: str, email: str, age: int):
    
    User_dico = {"id": user_id, "pseudo": pseudo, "name": name, "firstname": firstname, "email": email, "age": age}
    return User_dico

def update_user(user_id: int, user: User, session: Session):
    session.add(user)
    session.commit()
    return {"message": "User updated", "user_id": user_id, "user": user}

def delete_user(user_id: int): return {"message": "User deleted", "user_id": user_id}

ph = PasswordHasher()
def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False

