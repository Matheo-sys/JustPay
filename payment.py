from pydantic import BaseModel
from datetime import datetime
import uuid

class Payment(BaseModel):
    id : str =  uuid.uuid4()    
    account_number: str
    user_id: int
    beneficiary_account_number: str
    date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount: int

