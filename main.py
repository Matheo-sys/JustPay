from fastapi import Depends, FastAPI, HTTPException
from user import User, Gender, Region, create_user, get_user, update_user, delete_user
from bankAccount import BankAccount, AccountType, Currency, create_primary_bank_account, create_secondary_bank_account, deposit_to_account, get_all_bank_accounts, update_bank_account, delete_bank_account, get_primary_bank_account, get_secondary_bank_account, list_of_bank_accounts
from beneficiary import Beneficiary, add_beneficiary, get_beneficiary, list_of_beneficiaries
from payment import Payment
import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from db.database import create_db_and_tables, get_session
from auth_routes import router as auth_router

from routes.bankAccount.route import app as bank_account_router

create_db_and_tables()

app = FastAPI()
app.include_router(auth_router)

app.include_router(bank_account_router, prefix="/bankaccount")

@app.get("/")
def read_root():
    return {"JUSTPAY"}


