from fastapi import FastAPI, HTTPException
from user import User, Gender, Region, create_user, get_user, update_user, delete_user, add_deposit
from bankAccount import BankAccount, AccountType, Currency, create_primary_bank_account, create_secondary_bank_account, get_all_bank_accounts, update_bank_account, delete_bank_account, get_primary_bank_account, get_secondary_bank_account, list_of_bank_accounts
from beneficiary import Beneficiary, create_beneficiary, get_beneficiary, list_of_beneficiaries
from payment import Payment
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer



app = FastAPI()

@app.get("/")
def read_root():
    return {"JUSTPAY"}

#Routes pour User

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


#Routes pour BankAccount

@app.post("/accounts/primary")
def create_primary_account_root(name: str, firstname: str, email: str, age: int, account_number: str, user_id: int):
    try:
        account = create_primary_bank_account(name, firstname, email, age, account_number, user_id)
        return {"message": "Primary account created", "account": account}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accounts/secondary")
def create_secondary_account_root(name: str, firstname: str, email: str, age: int, account_number: str, user_id: int):
    try:
        account = create_secondary_bank_account(name, firstname, email, age, account_number, user_id)
        return {"message": "Secondary account created", "account": account}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts/primary")
def get_primary_account_route(name: str, firstname: str, email: str, age: int, account_number: int, balance: float, account_type: AccountType, currency: Currency, user_id: int):
    return get_primary_bank_account(name, firstname, email, age, account_number, balance, account_type, currency, user_id)

@app.get("/accounts/secondary")
def get_secondary_account_route(name: str, firstname: str, email: str, age: int, account_number: int, balance: float, account_type: AccountType, currency: Currency, user_id: int):
    return get_secondary_bank_account(name, firstname, email, age, account_number, balance, account_type, currency, user_id)

#Routes pour Beneficiary

@app.post("/beneficiaries")
def create_beneficiary_route(user_id: int, name: str, account_number: str):
    beneficiary = create_beneficiary(user_id, name, account_number)
    list_of_beneficiaries.append(beneficiary)
    return {"message": "Beneficiary created", "beneficiary": beneficiary}

