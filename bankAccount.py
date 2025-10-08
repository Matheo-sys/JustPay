from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from beneficiary import *
from db.database import Session
from db.models import BankAccount

class AccountType(int, Enum):
    principal = 1
    secondary = 0

class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"

class status(str, Enum):
    active = "active"
    inactive = "inactive"
    closed = "closed"

list_of_bank_accounts = []

def get_primary_bank_account(user_id: str, session: Session):
    
    
    account = session.exec(BankAccount).filter_by(user_id=user_id, account_type=AccountType.principal).first()
    if account:
        return {
            "message": "Bank account details",
            "account_id": account.account_number,
            "name": account.name,
            "firstname": account.firstname,
            "email": account.email,
            "age": account.age,
            "balance": account.balance,
            "currency": account.currency
        }
    else:
        return {"message": "Primary bank account not found", "account_id": None}
    
def get_secondary_bank_account(user_id: str, session: Session):
    
    accounts = session.exec(BankAccount).filter_by(user_id=user_id, account_type=AccountType.secondary).all()
    if accounts:
        account_list = []
        for account in accounts:
            account_list.append({
                "account_id": account.account_number,
                "name": account.name,
                "firstname": account.firstname,
                "email": account.email,
                "age": account.age,
                "balance": account.balance,
                "currency": account.currency
            })
        return {
            "message": "Secondary bank accounts details",
            "accounts": account_list
        }
    else:
        return {"message": "No secondary bank accounts found", "accounts": []}
    
def get_all_bank_accounts(user_id: str, session: Session):

    accounts = session.exec(BankAccount).filter_by(user_id=user_id).order_by(BankAccount.created_at.desc()).all()
    account_list = []
    for account in accounts:
        account_list.append({
            "account_id": account.account_number,
            "balance": cents_to_euros(account.balance),
            "created_at": account.created_at
        })
    return {
        "message": "List of user bank accounts",
        "accounts": account_list
    }

def update_bank_account(account_id: int, updated_data: dict, session: Session):

    account = session.exec(BankAccount).filter_by(account_number=account_id).first()
    if not account:
        return {"message": "Bank account not found", "account_id": account_id}
    for key, value in updated_data.items():
        setattr(account, key, value)
    session.commit()
    return {"message": "Bank account updated", "account_id": account_id, "account": account}

def delete_bank_account(account_id: int, session: Session):

    account = session.exec(BankAccount).filter_by(account_number=account_id).first()
    if not account:
        return {"message": "Bank account not found", "account_id": account_id}
    session.delete(account)
    session.commit()
    return {"message": "Bank account deleted", "account_id": account_id}

def create_primary_bank_account(name: str, firstname: str, email: str, age: int, account_number: str, user_id: str, session: Session):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
        
    bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=account_number, account_type=1, user_id=user_id)
    list_of_bank_accounts.append(bankUser)
    session.add(bankUser)
    session.commit()
    return bankUser

def create_secondary_bank_account(name: str, firstname: str, email: str, age: int, account_number: str, user_id: str, session: Session):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
    
    if list_of_bank_accounts.count >= 5:
        raise ValueError("User cannot have more than 5 bank accounts.")
        
    bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=account_number, balance=0 ,account_type=0, user_id=user_id)
    list_of_bank_accounts.append(bankUser)
    session.add(bankUser)
    session.commit()
    return bankUser

def cents_to_euros(cents: int):
    euros = cents / 100
    return euros

def euros_to_cents(euros: float):
    cents = int(euros * 100)
    return cents

def get_account_balance(account_id: int, session: Session):
    """
    Retourne les informations du compte et le solde.
    """
    account = session.exec(BankAccount).filter_by(account_number=account_id).first()
    if not account:
        return {"message": "Bank account not found", "account_id": account_id, "balance": None}
    return {
        "message": "Account details",
        "account_id": account.account_number,
        "name": account.name,
        "firstname": account.firstname,
        "email": account.email,
        "age": account.age,
        "balance": cents_to_euros(account.balance),
        "currency": account.currency,
        "status": account.status
    }

def deposit_to_account(account_id: int, amount: int, session: Session):

    account = session.exec(BankAccount).filter_by(account_number=account_id).first()
    if not account:
        return {"message": "Bank account not found", "account_id": account_id}
    if amount <= 0:
        return {"message": "Deposit amount must be positive", "account_id": account_id}
    account.balance += euros_to_cents(amount)
    session.commit()
    return {"message": "Deposit successful", "account_id": account_id, "new_balance": cents_to_euros(account.balance)}

def close_bank_account(account_id: int, user_id: str, session: Session):

    account = session.exec(BankAccount).filter_by(account_number=account_id, user_id=user_id).first()
    if not account:
        return {"message": "Bank account not found", "account_id": account_id}
    if account.account_type == AccountType.principal:
        return {"message": "Primary account cannot be closed", "account_id": account_id}
    if account.status == status.closed:
        return {"message": "Account already closed", "account_id": account_id}

    if hasattr(account, "has_pending_transactions") and account.has_pending_transactions:
        return {"message": "Account has pending transactions", "account_id": account_id}

    primary_account_data = get_primary_bank_account(user_id, session)
    if not primary_account_data or not primary_account_data.get("account_id"):
        return {"message": "Primary account not found for transfer", "account_id": account_id}
    primary_account = session.exec(BankAccount).filter_by(account_number=primary_account_data["account_id"]).first()
    if not primary_account:
        return {"message": "Primary account not found for transfer", "account_id": account_id}

    if account.balance > 0:
        primary_account.balance += account.balance
        account.balance = 0

    account.status = status.closed
    session.commit()
    return {"message": "Bank account closed", "account_id": account_id}
