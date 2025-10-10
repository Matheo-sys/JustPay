from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from argon2 import PasswordHasher
from db.database import get_session
from user import create_user, User
from auth import hasher_password, verifier_password, creer_token, find_user_by_email, get_current_user, validate_age,validate_gender,validate_nom,validate_password,validate_pseudo,validate_region,UserResponse, Inscription, Connexion
from pydantic import EmailStr

app = APIRouter(tags=["Auth"])

SECRET_KEY = "123456"
ALGORITHM = "HS256"
ph = PasswordHasher()
bearer = HTTPBearer()

@app.post("/inscription", response_model=UserResponse, status_code=201)
def inscription(pseudo: str,name: str, firstname: str, password: str, email: EmailStr, age: int, region: str, gender: str, session: Session = Depends(get_session)
):

    validate_pseudo(pseudo)
    
    validate_nom(name, "name")

    validate_nom(firstname, "firstname")
    
    validate_password(password)
    
    validate_age(age)
    
    validate_region(region)
    
    validate_gender(gender)

    user_existe = find_user_by_email(email, session)
    if user_existe:
        raise HTTPException(
            status_code=400,
            detail="Cet email est déjà utilisé"
        )
    
    if age < 18:
        raise HTTPException(
            status_code=400,
            detail="Vous devez avoir au moins 18 ans pour ouvrir un compte bancaire."
    )
    
    password_hashe = hasher_password(password)
    
    nouveau_user = create_user(
        pseudo=pseudo,
        name=name,
        firstname=firstname,
        password=password_hashe,
        email=email,
        age=age,
        region=region,
        gender=gender,
        session=session
    )

    session.add(nouveau_user)
    session.commit()
    session.refresh(nouveau_user)
    
    return nouveau_user


@app.post("/connexion")
def connexion(email: str, password: str,session: Session = Depends(get_session)
):
    user = find_user_by_email(email, session)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )
    
    password_correct = verifier_password(user.hashed_password, password)
    
    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )
    
    token = creer_token(user.id, user.email)
    
    return {
        "token": token,
        "type": "bearer"
    }


@app.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user