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
def inscription(user: Inscription, session: Session = Depends(get_session)):

    validate_pseudo(user.pseudo)
    validate_nom(user.name, "name")
    validate_nom(user.firstname, "firstname")
    validate_password(user.password)
    validate_age(user.age)
    validate_region(user.region)
    validate_gender(user.gender)

    user_existe = find_user_by_email(user.email, session)
    if user_existe:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    if user.age < 18:
        raise HTTPException(
            status_code=400,
            detail="Vous devez avoir au moins 18 ans pour ouvrir un compte bancaire."
        )

    password_hashe = hasher_password(user.password)

    nouveau_user = create_user(
        pseudo=user.pseudo,
        name=user.name,
        firstname=user.firstname,
        password=password_hashe,
        email=user.email,
        age=user.age,
        region=user.region,
        gender=user.gender,
        session=session
    )

    session.add(nouveau_user)
    session.commit()
    session.refresh(nouveau_user)

    return nouveau_user


@app.post("/connexion")
def connexion(payload: Connexion, session: Session = Depends(get_session)):
    email = payload.email
    password = payload.password

    user = find_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    password_correct = verifier_password(user.hashed_password, password)
    if not password_correct:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    token = creer_token(user.id, user.email)
    return {"token": token, "type": "bearer"}


@app.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user