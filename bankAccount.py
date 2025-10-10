from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from beneficiary import *
from db.database import Session
from db.models import BankAccount
from sqlmodel import select
import uuid
import threading
import time


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
    statement = select(BankAccount).filter_by(user_id=user_id, account_type=AccountType.principal)
    account = session.exec(statement).first()
    if account:
        return {
            "message": "Bank account details",
            "account_number": account.account_number,
            "name": account.name,
            "firstname": account.firstname,
            "email": account.email,
            "age": account.age,
            "balance": account.balance,
            "currency": account.currency
        }
    else:
        return {"message": "Primary bank account not found", "account_number": None}
    
def get_secondary_bank_account(user_id: str, session: Session):
    statement = select(BankAccount).filter_by(user_id=user_id, account_type=AccountType.secondary)
    accounts = session.exec(statement).all()
    if accounts:
        account_list = []
        for account in accounts:
            account_list.append({
                "account_number": account.account_number,
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

    statement = select(BankAccount).filter_by(user_id=user_id).order_by(BankAccount.created_at.desc())
    accounts = session.exec(statement).all()
    account_list = []
    for account in accounts:
        account_list.append({
            "account_number": account.account_number,
            "balance": cents_to_euros(account.balance),
            "created_at": account.created_at
        })
    return {
        "message": "List of user bank accounts",
        "accounts": account_list
    }

def update_bank_account(account_number: int, updated_data: dict, session: Session):

    statement = select(BankAccount).filter_by(account_number=account_number)
    account = session.exec(statement).first()
    if not account:
        return {"message": "Bank account not found", "account_number": account_number}
    for key, value in updated_data.items():
        setattr(account, key, value)
    session.commit()
    return {"message": "Bank account updated", "account_number": account_number, "account": account}

def delete_bank_account(account_number: str, session: Session):

    statement = select(BankAccount).filter_by(account_number=account_number)
    account = session.exec(statement).first()
    if not account:
        return {"message": "Bank account not found", "account_number": account_number}
    session.delete(account)
    session.commit()
    return {"message": "Bank account deleted", "account_number": account_number}

def create_primary_bank_account(name: str, firstname: str, email: str, age: int, user_id: str, session: Session):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
        
    bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number= str(uuid.uuid4()), account_type=1, user_id=user_id)
    list_of_bank_accounts.append(bankUser)
    session.add(bankUser)
    session.commit()
    return bankUser

def create_secondary_bank_account(name: str, firstname: str, email: str, age: int, user_id: str, session: Session):
    if age < 18:
        raise ValueError("User must be at least 18 years old to create a bank account.")
    
    if not name or not firstname or not email:
        raise ValueError("Name, firstname, and email cannot be empty.")
    
    if len(list_of_bank_accounts) >= 5:
        raise ValueError("User cannot have more than 5 bank accounts.")
        
    bankUser = BankAccount(name=name, firstname=firstname, email=email, age=age, account_number=str(uuid.uuid4()), balance=0 ,account_type=0, user_id=user_id)
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

def get_account_balance(account_number: str, session: Session):
    """
    Retourne les informations du compte et le solde.
    """
    statement = select(BankAccount).filter_by(account_number=account_number)
    account = session.exec(statement).first()
    if not account:
        return {"message": "Bank account not found", "account_number": account_number, "balance": None}
    return {
        "message": "Account details",
        "account_number": account.account_number,
        "name": account.name,
        "firstname": account.firstname,
        "email": account.email,
        "age": account.age,
        "balance": cents_to_euros(account.balance),
        "currency": account.currency,
        "status": account.status
    }

def deposit_to_account(account_number: str, amount: int, session: Session):

    statement = select(BankAccount).filter_by(account_number=account_number)
    account = session.exec(statement).first()
    if not account:
        return {"message": "Bank account not found", "account_number": account_number}
    if amount <= 0:
        return {"message": "Deposit amount must be positive", "account_number": account_number}
    account.balance += euros_to_cents(amount)
    session.commit()
    return {"message": "Deposit successful", "account_number": account_number, "new_balance": cents_to_euros(account.balance)}

def close_bank_account(account_number: int, user_id: str, session: Session):

    statement = select(BankAccount).filter_by(account_number=account_number)
    account = session.exec(statement).first()
    if not account:
        return {"message": "Bank account not found", "account_number": account_number}
    if account.account_type == AccountType.principal:
        return {"message": "Primary account cannot be closed", "account_number": account_number}
    if account.status == status.closed:
        return {"message": "Account already closed", "account_number": account_number}

    if hasattr(account, "has_pending_transactions") and account.has_pending_transactions:
        return {"message": "Account has pending transactions", "account_number": account_number}

    primary_account_data = get_primary_bank_account(user_id, session)
    if not primary_account_data or not primary_account_data.get("account_number"):
        return {"message": "Primary account not found for transfer", "account_number": account_number}
    statement = select(BankAccount).filter_by(account_number=primary_account_data["account_number"])
    primary_account = session.exec(statement).first()
    if not primary_account:
        return {"message": "Primary account not found for transfer", "account_number": account_number}

    if account.balance > 0:
        primary_account.balance += account.balance
        account.balance = 0

    account.status = status.closed
    session.commit()
    return {"message": "Bank account closed", "account_number": account_number}

def transfer_secondary_excess_to_primary(account_number: str, session: Session):
    """
    Si la balance d'un compte secondaire dépasse 50 000€, transfère le surplus sur le compte principal associé.
    """
    MAX_BALANCE_CENTS = euros_to_cents(50000)

    statement = select(BankAccount).filter_by(account_number=account_number, account_type=AccountType.secondary)
    account = session.exec(statement).first()
    if not account:
        return {"message": "Secondary bank account not found", "account_number": account_number}
    if account.balance > MAX_BALANCE_CENTS:
        surplus = account.balance - MAX_BALANCE_CENTS
        # Récupérer le compte principal associé
        primary_account_data = get_primary_bank_account(account.user_id, session)
        if not primary_account_data or not primary_account_data.get("account_number"):
            return {"message": "Primary account not found for transfer", "account_number": account_number}
        statement = select(BankAccount).filter_by(account_number=primary_account_data["account_number"])
        primary_account = session.exec(statement).first()
        if not primary_account:
            return {"message": "Primary account not found for transfer", "account_number": account_number}
 
        primary_account.balance += surplus
        account.balance = MAX_BALANCE_CENTS
        session.commit()
        return {
            "message": "Surplus transferred to primary account",
            "secondary_account_number": account_number,
            "primary_account_number": primary_account.account_number,
            "transferred_amount": cents_to_euros(surplus),
            "secondary_new_balance": cents_to_euros(account.balance),
            "primary_new_balance": cents_to_euros(primary_account.balance)
        }
    else:
        return {
            "message": "No surplus to transfer",
            "secondary_account_number": account_number,
            "balance": cents_to_euros(account.balance)
        }
    

def schedule_transfer_excess(account_number: str, session: Session):
    def run_task():
        while True:
            transfer_secondary_excess_to_primary(account_number, session)
            time.sleep(300)  # 300 secondes = 5 minutes
    thread = threading.Thread(target=run_task, daemon=True)
    thread.start()

