from pydantic import BaseModel
from datetime import datetime
import uuid
from enum import Enum
from bankAccount import cents_to_euros, euros_to_cents

class Payment(BaseModel):
    id : str =  uuid.uuid4()    
    account_number: str
    user_id: int
    beneficiary_account_number: str
    date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount: int

class OperationType(str, Enum):
    INTERNAL_TRANSFER = "virement interne"
    EXTERNAL_TRANSFER = "virement externe"

class Operation(BaseModel):
    id : str =  uuid.uuid4()    
    payment_id: str
    operation_type: OperationType
    status: str = "pending"
    date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount: int

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class Beneficiary(BaseModel):
    id : str =  uuid.uuid4()    
    user_id: int
    name: str
    account_number: str 


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

    return account_transactions
      




"""
virement interne
virement externe
liste des beneficiaries
"""