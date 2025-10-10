from pydantic import BaseModel
from datetime import datetime
import uuid
from enum import Enum
from bankAccount import cents_to_euros, euros_to_cents
from db.database import Session, get_session
from db.models import Payment, BankAccount
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

def create_transfer(user_id: str, account_number: str, beneficiary_account_number: str, amount: int, session: Session):
    session = next(get_session())
    # Vérifier que le compte appartient à l'utilisateur
    account = session.exec(
        select(BankAccount).where(
            BankAccount.account_number == account_number,
            BankAccount.user_id == user_id
        )
    ).first()
    if not account:
        raise PermissionError("L'utilisateur n'est pas le propriétaire du compte.")

    # Vérifier que le compte bénéficiaire existe (peut être secondaire ou principal, mais pas forcément un bénéficiaire enregistré)
    beneficiary_account = session.exec(
        select(BankAccount).where(BankAccount.account_number == beneficiary_account_number)
    ).first()
    if not beneficiary_account:
        raise ValueError("Le compte bénéficiaire n'existe pas.")

    # Vérifier que le solde est suffisant
    if account.balance < amount:
        raise ValueError("Solde insuffisant.")

    # Créer le paiement
    
    if beneficiary_account.user_id == user_id:
        payment = create_internal_transfer(user_id, account_number, beneficiary_account_number, amount)
    else:
        payment = create_external_transfer(user_id, account_number, beneficiary_account_number, amount)

    account.balance -= amount
    beneficiary_account.balance += amount
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

def create_internal_transfer(user_id: str, account_number: str, beneficiary_account_number: str, amount: int):

        payment = Payment(
        account_number=account_number,
        user_id=user_id,
        beneficiary_account_number=beneficiary_account_number,
        amount=cents_to_euros(amount),
        date=datetime.now(timezone.utc),
        status=PaymentStatus.PENDING,
        operation_type=OperationType.INTERNAL_TRANSFER
    )
        return payment

def create_external_transfer(user_id: str, account_number: str, beneficiary_account_number: str, amount: int):

        payment = Payment(
        account_number=account_number,
        user_id=user_id,
        beneficiary_account_number=beneficiary_account_number,
        amount=cents_to_euros(amount),
        date=datetime.now(timezone.utc),
        status=PaymentStatus.PENDING,
        operation_type=OperationType.EXTERNAL_TRANSFER
    )
        return payment

def update_account_balance(account_number: str, amount: int, is_debit: bool):
    session = next(get_session())
    account = session.exec(select(BankAccount).where(BankAccount.account_number == account_number)).first()
    if not account:
        raise ValueError("Compte introuvable.")
    if is_debit:
        account.balance -= amount
    else:
        account.balance += amount
    session.commit()

def get_account_transactions(account_number: str, session: Session):
    payments = session.exec(
        select(Payment).where(Payment.account_number == account_number)
    ).all()
    payments.sort(key=lambda x: x.date, reverse=True)
    return payments

def cancel_payment(payment_id: str):
    session = next(get_session())
    with get_session() as session:
        payment = session.exec(select(Payment).where(Payment.id == payment_id)).first()
        if payment:
            payment.status = "cancelled"
            session.commit()

def get_payment_details(payment_id: str):
    session = next(get_session())
    payment = session.exec(select(Payment).where(Payment.id == payment_id)).first()
    if not payment:
        return None
    return payment

from datetime import datetime, timedelta

def cancel_payment(user_id: int, payment_id: str) -> bool:
    # . Récupérer la transaction
    payment = get_payment_details(payment_id)
    if not payment:
        return False  # Transaction introuvable

    #  Vérifier que l'utilisateur est le propriétaire de la transaction
    if payment.user_id != user_id:
        return False  # L'utilisateur n'est pas autorisé

    #  Vérifier que la transaction est en statut PENDING
    if payment.status != PaymentStatus.PENDING:
        return False  # Impossible d'annuler une transaction déjà complétée ou annulée
    
    """    #  Vérifier que l'annulation intervient dans les 5 secondes
    if (datetime.now() - payment.date) > timedelta(seconds=5):
        return False  # Délai d'annulation dépassé 
    """
    
    #  Mettre à jour les soldes (annuler le débit/crédit)
    if payment.operation_type == OperationType.INTERNAL_TRANSFER:
        # Annuler le débit du compte source
        update_account_balance(payment.account_number, payment.amount, is_debit=False)
        # Annuler le crédit du compte destinataire
        update_account_balance(payment.beneficiary_account_number, payment.amount, is_debit=True)
    elif payment.operation_type == OperationType.EXTERNAL_TRANSFER:
        # Annuler le débit du compte source (montant + frais)
        update_account_balance(payment.account_number, payment.amount, is_debit=False)

    #  Mettre à jour le statut de la transaction
    payment.status = PaymentStatus.CANCELLED

    return True  # Annulation réussie





