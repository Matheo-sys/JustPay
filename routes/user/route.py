from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session
from db.database import get_session
from db.models import User
from user import create_user, get_user, Gender, Region
from bankAccount import create_primary_bank_account, deposit_to_account


app = FastAPI()

@app.post("/users")
def create_user_root(pseudo: str, name: str, firstname: str, password: str, email: str, age: int, region: Region, gender: Gender, session = Depends(get_session)):
    try:
        user = create_user(pseudo, name, firstname, password, email, age, region, gender, session)
        return {"message": "User created", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/users/{user_id}")
def get_user_root(user_id: int, session: Session = Depends(get_session)):
    user_data = get_user(user_id, session)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@app.post("/users/deposit")
def add_deposit_root(account_id: str, amount: int, session = Depends(get_session)):
    result = deposit_to_account(account_id, amount, session)
    return result