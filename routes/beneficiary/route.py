from fastapi import APIRouter, Depends, HTTPException
from db.database import get_session
from sqlmodel import Session
from beneficiary import (add_beneficiary, get_beneficiary, update_beneficiary, delete_beneficiary, list_of_beneficiaries,)

app = APIRouter(tags=["Beneficiary"])

@app.post("/")
def create_beneficiary(user_id: str, name: str, account_number: str, session: Session = Depends(get_session)):
    try:
        beneficiary = add_beneficiary(user_id, name, account_number, session)
        return {
            "message": "Bénéficiaire ajouté.",
            "beneficiary": {
                "id": beneficiary.id,
                "name": beneficiary.name,
                "account_number": beneficiary.account_number,
                "date_added": getattr(beneficiary, "date_added", None)
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/{beneficiary_id}")
def read_beneficiary(beneficiary_id: str, session: Session = Depends(get_session)):
    try:
        beneficiary = get_beneficiary(beneficiary_id, session)
        return {
            "id": beneficiary.id,
            "name": beneficiary.name,
            "account_number": beneficiary.account_number,
            "date_added": getattr(beneficiary, "date_added", None)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/{beneficiary_id}")
def delete_beneficiary_route(beneficiary_id: str, session: Session = Depends(get_session)):
    try:
        return delete_beneficiary(beneficiary_id, session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/user/{user_id}")
def list_beneficiaries_route(user_id: str, session: Session = Depends(get_session)):
    return list_of_beneficiaries(user_id, session)

