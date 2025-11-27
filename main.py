from fastapi import FastAPI
from db.database import create_db_and_tables
from routes.user.route import app as user_router
from routes.bankAccount.route import app as bank_account_router
from routes.beneficiary.route import app as beneficiary_router
from routes.payement.route import app as payment_router
from routes.auth.route import app as auth_router
from fastapi.middleware.cors import CORSMiddleware

create_db_and_tables()

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")
app.include_router(bank_account_router, prefix="/bankaccount")
app.include_router(beneficiary_router, prefix="/beneficiaries")
app.include_router(payment_router, prefix="/payments")

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,        
    allow_methods=["*"],           
    allow_headers=["*"],          
)

