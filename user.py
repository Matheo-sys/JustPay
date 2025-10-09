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

def create_user(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: Region, gender: Gender, session: Session):    
    user = User(
        pseudo=pseudo, 
        name=name, 
        firstname=firstname, 
        hashed_password=password,
        email=email, 
        age=age, 
        region=region,
        gender=gender
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    create_primary_bank_account(
        name=name, 
        firstname=firstname, 
        email=email, 
        age=age, 
        user_id=str(user.id),
        session=session
    )
    return user

def get_user(user_id: int, session: Session):
    user = session.get(User, user_id)
    if not user:
        return None
    return {
        "user_id": user.id,
        "pseudo": user.pseudo,
        "name": user.name,
        "firstname": user.firstname,
        "email": user.email,
        "age": user.age,
        "region": user.region,
        "gender": user.gender
    }

def update_user(user_id: int, user: User, session: Session):
    session.add(user)
    session.commit()
    return {"message": "User updated", "user_id": user_id, "user": user}

def delete_user(user_id: int): return {"message": "User deleted", "user_id": user_id}

