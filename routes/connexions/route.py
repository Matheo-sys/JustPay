from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from fastapi import APIRouter

app = APIRouter(tags=[""])

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class EmailChange(BaseModel):
    email: EmailStr


@app.put("/user/change-password")
def change_password(data: PasswordChange):
    # Exemple de vérification
    if data.current_password != "1234":
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")
    
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Les nouveaux mots de passe ne correspondent pas")

    return {"message": "Mot de passe modifié !"}


@app.put("/user/change-email")
def change_email(data: EmailChange):
    return {"message": f"Email mis à jour : {data.email}"}
