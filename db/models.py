from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime, timezone


class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    pseudo: str
    name: str
    firstname: str
    hashed_password: str
    email: str = Field(index=True, unique=True)
    age: int
    region: str
    gender: str

    bank_accounts: List["BankAccount"] = Relationship(back_populates="user")
    beneficiaries: List["Beneficiary"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user")

class BankAccount(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name: str
    firstname: str
    email: str
    age: int
    account_number: str = Field(index=True, unique=True) #ajouter UUID
    balance: int = 10000 # Balance in cents
    account_type: int
    currency: str = "EUR"
    status: str = "active"
    user_id: Optional[str] = Field(foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="bank_accounts")

class Beneficiary(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    user_id: Optional[str] = Field(foreign_key="user.id")
    name: str
    account_number: str

    user: Optional[User] = Relationship(back_populates="beneficiaries")

class Payment(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    account_number: str = Field(foreign_key="bankaccount.account_number")
    user_id: Optional[str] = Field(foreign_key="user.id")
    beneficiary_account_number: str = Field(foreign_key="beneficiary.account_number")
    date: datetime = Field(default_factory=datetime.now(timezone.utc))
    amount: int

    user: Optional[User] = Relationship(back_populates="payments")

class Operation(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    payment_id: Optional[str] = Field(foreign_key="payment.id")
    operation_type: str
    status: str = "pending"
    date: datetime = Field(default_factory=datetime.now(timezone.utc))
    amount: int

    payment: Optional[Payment] = Relationship()