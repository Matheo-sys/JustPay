from fastapi import Depends, FastAPI, HTTPException, APIRouter
from bankAccount import (
    create_primary_bank_account,
    create_secondary_bank_account,
    get_primary_bank_account,
    get_secondary_bank_account,
    get_all_bank_accounts,
    update_bank_account,
    delete_bank_account,
    get_account_balance,
    deposit_to_account,
    close_bank_account,
    AccountType,
    Currency,
    list_of_bank_accounts,
)
from db.database import get_session

app = APIRouter()

# Création compte principal
@app.post("/accounts/primary")
def create_primary_account(
    name: str,
    firstname: str,
    email: str,
    age: int,
    user_id: str,
    session=Depends(get_session)
):
    try:
        account = create_primary_bank_account(name, firstname, email, age, user_id, session)
        return {"message": "Primary account created", "account": account.account_number}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Création compte secondaire
@app.post("/accounts/secondary")
def create_secondary_account(
    name: str,
    firstname: str,
    email: str,
    age: int,
    user_id: str,
    session=Depends(get_session)
):
    try:
        account = create_secondary_bank_account(name, firstname, email, age, user_id, session)
        return {"message": "Secondary account created", "account": account.account_number}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Récupérer compte principal
@app.get("/accounts/primary/{user_id}")
def get_primary_account(user_id: str, session=Depends(get_session)):
    return get_primary_bank_account(user_id, session)

# Récupérer comptes secondaires
@app.get("/accounts/secondary/{user_id}")
def get_secondary_accounts(user_id: str, session=Depends(get_session)):
    return get_secondary_bank_account(user_id, session)

# Récupérer tous les comptes
@app.get("/accounts/")
def get_all_accounts():
    return get_all_bank_accounts()

# Mettre à jour un compte

"""@app.put("/accounts/{account_number}")
def update_account(account_number: str, updated_data: dict, session=Depends(get_session)):
    return update_bank_account(account_number, updated_data, session)
"""

# Supprimer un compte
@app.delete("/accounts/{account_number}")
def delete_account(account_number: str, session=Depends(get_session)):
    return delete_bank_account(account_number, session)

# Consulter le solde et infos du compte
@app.get("/accounts/balance/{account_number}")
def get_balance(account_number: str, session=Depends(get_session)):
    return get_account_balance(account_number, session)

# Déposer sur un compte
@app.post("/accounts/deposit")
def deposit(account_number: str, amount: int, session=Depends(get_session)):
    return deposit_to_account(account_number, amount, session)

# Clôturer un compte
@app.post("/accounts/close")
def close_account(account_number: str, user_id: str, session=Depends(get_session)):
    return close_bank_account(account_number, user_id, session)