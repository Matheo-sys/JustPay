from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pseudo = Column(String, nullable=False)
    name = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    bank_accounts = relationship("BankAccount", back_populates="user")
    beneficiaries = relationship("Beneficiary", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class BankAccount(Base):
    __tablename__ = 'bank_accounts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    account_number = Column(String, unique=True, nullable=False)
    balance = Column(Integer, default=10000)
    account_type = Column(Integer, nullable=False)
    currency = Column(String, default="EUR")
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    user = relationship("User", back_populates="bank_accounts")

class Beneficiary(Base):
    __tablename__ = 'beneficiaries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)

    user = relationship("User", back_populates="beneficiaries")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_number = Column(String, ForeignKey('bank_accounts.account_number'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    beneficiary_account_number = Column(String, ForeignKey('beneficiaries.account_number'))
    date = Column(DateTime)
    amount = Column(Integer, nullable=False)

    user = relationship("User", back_populates="payments")

class Operation(Base):
    __tablename__ = 'operations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey('payments.id'))
    operation_type = Column(String, nullable=False)
    status = Column(String, default="pending")
    date = Column(DateTime)
    amount = Column(Integer, nullable=False)

    payment = relationship("Payment")