from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    male = "male"
    female = "female"

class Region(str, Enum):
    Europe = "Europe"
    America = "America"

class UserSchema(BaseModel):
    id: UUID
    pseudo: str
    name: str
    firstname: str
    hashed_password: str
    email: str
    age: int
    region: Region
    gender: Gender

class BankAccountSchema(BaseModel):
    id: UUID
    name: str
    firstname: str
    email: str
    age: int
    account_number: str
    balance: int
    account_type: int
    currency: str
    user_id: UUID

class BeneficiarySchema(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    account_number: str

class PaymentSchema(BaseModel):
    id: UUID
    account_number: str
    user_id: UUID
    beneficiary_account_number: str
    date: datetime
    amount: int

class OperationSchema(BaseModel):
    id: UUID
    payment_id: UUID
    operation_type: str
    status: str
    date: datetime
    amount: int