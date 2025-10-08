from pydantic import BaseModel
from datetime import datetime
import uuid
from enum import Enum
from bankAccount import cents_to_euros, euros_to_cents
from db.database import Session, get_session
from db.models import Payment, Beneficiary, Operation


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class OperationType(str, Enum):
    INTERNAL_TRANSFER = "virement interne"
    EXTERNAL_TRANSFER = "virement externe"


def create_payment(user_id: int, account_number: str, beneficiary_account_number: str, amount: int) -> Payment:
    payment = Payment(
        account_number=account_number,
        user_id=user_id,
        beneficiary_account_number=beneficiary_account_number,
        amount=amount
    )
    
    return payment

def get_payment_details(payment_id: str) -> Payment:
    for payment in payments_db:
        if payment.id == payment_id:
            return payment
    return None

def get_account_transactions(account_number: str) -> list[Payment]:
    account_transactions = [payment for payment in payments_db if payment.account_number == account_number]

    account_transactions.sort(key=lambda x: x.date, reverse=True)
    return account_transactions
      
def cancel_payment() -> None:
    pass



"""
virement interne
virement externe
liste des beneficiaires
annuler transaction 
visualiser le détail/info d’une transaction
"""

