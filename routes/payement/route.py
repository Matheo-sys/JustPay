from fastapi import APIRouter, Depends, HTTPException
from db.database import get_session
from sqlmodel import Session
from payment import (
    create_internal_transfer,
    create_external_transfer,
    get_payment_details,
    get_account_transactions,
    cancel_payment,
)

app = APIRouter()

@app.post("/internal")
def internal_transfer(
    user_id: str,
    account_number: str,
    beneficiary_account_number: str,
    amount: int,
    session: Session = Depends(get_session)
):
    try:
        payment = create_internal_transfer(user_id, account_number, beneficiary_account_number, amount)
        return payment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/external")
def external_transfer(
    user_id: str,
    account_number: str,
    beneficiary_account_number: str,
    amount: int,
    bic_swift: str,
    fees: int = 0,
    session: Session = Depends(get_session)
):
    try:
        payment = create_external_transfer(user_id, account_number, beneficiary_account_number, amount, bic_swift, fees)
        return payment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/{payment_id}")
def payment_details(payment_id: str, session: Session = Depends(get_session)):
    payment = get_payment_details(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Transaction introuvable.")
    return payment

@app.get("/account/{account_number}")
def account_transactions(account_number: str, session: Session = Depends(get_session)):
    payments = get_account_transactions(account_number)
    return payments

@app.post("/cancel")
def cancel_payment_route(user_id: str, payment_id: str, session: Session = Depends(get_session)):
    success = cancel_payment(user_id, payment_id)
    if not success:
        raise HTTPException(status_code=400, detail="Impossible d'annuler la transaction.")
    return {"message": "Transaction annulée avec succès."}