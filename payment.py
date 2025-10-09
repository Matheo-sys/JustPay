from pydantic import BaseModel
from datetime import datetime
import uuid
from enum import Enum
from bankAccount import cents_to_euros, euros_to_cents
from db.database import Session, get_session
from db.models import Payment, Beneficiary, Operation, BankAccount
from datetime import datetime, timezone
from sqlmodel import select

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class OperationType(str, Enum):
    INTERNAL_TRANSFER = "virement interne"
    EXTERNAL_TRANSFER = "virement externe"

class Payment(BaseModel):
    id: str = str(uuid.uuid4())
    account_number: str
    user_id: int
    beneficiary_account_number: str
    amount: int
    date: datetime = datetime.now()
    status: PaymentStatus = PaymentStatus.PENDING
    operation_type: OperationType
    bic_swift: str | None = None  # Pour les virements externes
    fees: int = 0  # centimes
    
def create_internal_transfer(user_id: str, account_number: str, beneficiary_account_number: str, amount: int):
    with get_session() as session:
        # Vérifier que le compte appartient à l'utilisateur
        account = session.exec(select(BankAccount).where(BankAccount.account_number == account_number, BankAccount.user_id == user_id)).first()
        if not account:
            raise PermissionError("L'utilisateur n'est pas le propriétaire du compte.")
        # Vérifier que le bénéficiaire existe
        beneficiary = session.exec(select(Beneficiary).where(Beneficiary.account_number == beneficiary_account_number)).first()
        if not beneficiary:
            raise ValueError("Bénéficiaire introuvable.")
        # Créer le paiement
        payment = Payment(
            account_number=account_number,
            user_id=user_id,
            beneficiary_account_number=beneficiary_account_number,
            amount=amount,
            date=datetime.now(timezone.utc)
        )
        session.add(payment)
        account.balance -= amount
        session.commit()
        session.refresh(payment)
        return payment

def create_external_transfer(user_id: str, account_number: str, beneficiary_account_number: str, amount: int, bic_swift: str, fees: int = 0):
    with get_session() as session:
        account = session.exec(select(BankAccount).where(BankAccount.account_number == account_number, BankAccount.user_id == user_id)).first()
        if not account:
            raise PermissionError("L'utilisateur n'est pas le propriétaire du compte.")
        beneficiary = session.exec(select(Beneficiary).where(Beneficiary.account_number == beneficiary_account_number)).first()
        if not beneficiary:
            raise ValueError("Bénéficiaire introuvable.")
        payment = Payment(
            account_number=account_number,
            user_id=user_id,
            beneficiary_account_number=beneficiary_account_number,
            amount=amount,
            date=datetime.now(timezone.utc)
        )
        session.add(payment)
        account.balance -= (amount + fees)
        session.commit()
        session.refresh(payment)
        return payment

def update_account_balance(account_number: str, amount: int, is_debit: bool):
    with get_session() as session:
        account = session.exec(select(BankAccount).where(BankAccount.account_number == account_number)).first()
        if not account:
            raise ValueError("Compte introuvable.")
        if is_debit:
            account.balance -= amount
        else:
            account.balance += amount
        session.commit()

def get_payment_details(payment_id: str):
    with get_session() as session:
        payment = session.exec(select(Payment).where(Payment.id == payment_id)).first()
        return payment

def get_account_transactions(account_number: str):
    with get_session() as session:
        payments = session.exec(select(Payment).where(Payment.account_number == account_number)).all()
        payments.sort(key=lambda x: x.date, reverse=True)
        return payments

def cancel_payment(payment_id: str):
    with get_session() as session:
        payment = session.exec(select(Payment).where(Payment.id == payment_id)).first()
        if payment:
            payment.status = "cancelled"
            session.commit()





"""
virement interne
virement externe
liste des beneficiaires
annuler transaction 
visualiser le détail/info d’une transaction


git add . 
git commit -m "message"
git pull
git push


"""

