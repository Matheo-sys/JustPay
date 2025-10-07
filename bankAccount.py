from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from beneficiary import *

class AccountType(int, Enum):
    principal = 1
    secondary = 0

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"

class BankAccount(BaseModel):
    name: str
    firstname: str
    email: str
    age: int
    account_number: str
    balance: int = 0
    account_type: AccountType = 1
    currency: str = "EUR"
    user_id: str

list_of_bank_accounts = []

def get_primary_bank_account(name: str, firstname: str, email: str, age: int, account_number: int, balance: float, account_type: AccountType, currency: Currency, user_id: str):
    
    for account in list_of_bank_accounts:
        if account.account_type == AccountType.principal:
            
            return {"message": "Bank account details", "account_id": account_number}

def get_secondary_bank_account(name: str, firstname: str, email: str, age: int, account_number: int, balance: float, account_type: AccountType, currency: Currency, user_id: str):
    
    return {"message": "Bank account details", "account_id": account_number}

def get_all_bank_accounts():    return list_of_bank_accounts

def update_bank_account(account_id  : int, account: BankAccount):    return {"message": "Bank account updated", "account_id": account_id, "account": account}
def delete_bank_account(account_id: int):    return {"message": "Bank account deleted", "account_id": account_id}


def create_bank_account(name: str, firstname: str, email: str, age: int, account_number: str, account_type: AccountType, user_id: str):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
    
    for account in list_of_bank_accounts:

        if account.email == email:
            raise ValueError("A bank account with this email already exists.")
        
        if account.account_type == AccountType.principal:
            bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=account_number, account_type=0, user_id=user_id)
        else:
            bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=account_number, account_type=1, user_id=user_id)

    list_of_bank_accounts.append(bankUser)
    return list_of_bank_accounts

"""
create primary bank account when creating user
or creat secondary bank account when user already has a primary bank account
"""

def create_primary_bank_account(name: str, firstname: str, email: str, age: int, account_number: str, user_id: str):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
    
    for account in list_of_bank_accounts:

        if account.email == email:
            raise ValueError("A bank account with this email already exists.")
        
        if account.account_type == AccountType.principal:
            raise ValueError("User already has a primary bank account.")
        
    bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=account_number, account_type=1, user_id=user_id)
    list_of_bank_accounts.append(bankUser)
    return bankUser

def create_secondary_bank_account(name: str, firstname: str, email: str, age: int, account_number: str, user_id: str):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
        
    bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=account_number, account_type=0, user_id=user_id)
    list_of_bank_accounts.append(bankUser)
    return bankUser