from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import uuid

class Beneficiary(BaseModel):
    name: str
    account_number: str 
    user_id: int = None

list_of_beneficiaries = []

def create_beneficiary(user_id, name: str, account_number: str): 
    
    beneficiary = Beneficiary(user_id = user_id, name=name, account_number=account_number)
    return beneficiary

def get_beneficiary(beneficiary : Beneficiary):    
    
    beneficiary_dico = {"name": beneficiary.name, "account_number": beneficiary.account_number}
    return beneficiary_dico
