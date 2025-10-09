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


def create_user(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: str, gender: str, session: Session):    
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

def get_user(user_id: str, session: Session):
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

def update_user(user_id: str, updated_data: dict, session: Session):
    user = session.get(User, user_id)
    if not user:
        return None
    for key, value in updated_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    session.commit()
    return user

def delete_user(user_id: str, session: Session):
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

