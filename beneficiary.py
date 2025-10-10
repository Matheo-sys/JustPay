from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import uuid
from db.models import Beneficiary, User, BankAccount
from db.database import get_session
from sqlmodel import select, Session
from datetime import datetime, timezone

list_of_beneficiaries = []


def get_beneficiary(beneficiary : Beneficiary):    
    
    beneficiary_dico = {"name": beneficiary.name, "account_number": beneficiary.account_number}
    return beneficiary_dico

def add_beneficiary(user_id: str, name: str, account_number: str, session: Session):
    # Vérifier que le nom est renseigné
    if not name:
        raise ValueError("Le nom du bénéficiaire doit être renseigné.")

    # Vérifier que le bénéficiaire n'est pas un des comptes de l'utilisateur
    user_accounts = session.exec(select(BankAccount).where(BankAccount.user_id == user_id)).all()
    if any(acc.account_number == account_number for acc in user_accounts):
        raise ValueError("Le bénéficiaire ne peut pas être un des comptes de l'utilisateur.")

    # Vérifier que le bénéficiaire n'existe pas déjà pour cet utilisateur
    existing = session.exec(
        select(Beneficiary).where(
            Beneficiary.user_id == user_id,
            Beneficiary.account_number == account_number
        )
    ).first()
    if existing:
        raise ValueError("Le bénéficiaire existe déjà.")

    # Vérifier que le compte existe dans la base
    account_exists = session.exec(select(BankAccount).where(BankAccount.account_number == account_number)).first()
    if not account_exists:
        raise ValueError("Le bénéficiaire doit exister.")

    beneficiary = Beneficiary(
        user_id=user_id,
        name=name,
        account_number=account_number,
        date_added=datetime.now(timezone.utc)
    )
    session.add(beneficiary)
    session.commit()
    session.refresh(beneficiary)
    return beneficiary

def get_beneficiary(beneficiary_id: str, session: Session):
    beneficiary = session.get(Beneficiary, beneficiary_id)
    if not beneficiary:
        raise ValueError("Bénéficiaire introuvable.")
    return beneficiary

def update_beneficiary(beneficiary_id: str, name: str, session: Session):
    beneficiary = session.get(Beneficiary, beneficiary_id)
    if not beneficiary:
        raise ValueError("Bénéficiaire introuvable.")
    if not name:
        raise ValueError("Le nom du bénéficiaire doit être renseigné.")
    beneficiary.name = name
    session.commit()
    session.refresh(beneficiary)
    return beneficiary

def delete_beneficiary(beneficiary_id: str, session: Session):
    beneficiary = session.get(Beneficiary, beneficiary_id)
    if not beneficiary:
        raise ValueError("Bénéficiaire introuvable.")
    session.delete(beneficiary)
    session.commit()
    return {"message": "Bénéficiaire supprimé.", "name": beneficiary.name}

def list_of_beneficiaries(user_id: str, session: Session):
    beneficiaries = session.exec(
        select(Beneficiary).where(Beneficiary.user_id == user_id)
    ).all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "account_number": b.account_number,
            "date_added": getattr(b, "date_added", None)
        }
        for b in beneficiaries
    ]