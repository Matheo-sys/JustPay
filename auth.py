from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from db.models import User
from db.database import get_session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from datetime import datetime, timedelta
from user import create_user
import re


SECRET_KEY = "123456"
ALGORITHM = "HS256"
ph = PasswordHasher()
bearer = HTTPBearer()


class Inscription(BaseModel):
    pseudo: str
    name: str
    firstname: str
    password: str
    email: EmailStr
    age: int
    region: str
    gender: str

class Connexion(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    pseudo: str
    name: str
    firstname: str
    email: str
    age: int
    region: str
    gender: str
    


def hasher_password(password: str) -> str:
    return ph.hash(password)

def verifier_password(password_hash: str, password_clair: str) -> bool:
    try:
        ph.verify(password_hash, password_clair)
        return True
    except VerifyMismatchError:
        return False

def creer_token(user_id: str, email: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=24)
    donnees = {
        "user_id": user_id,
        "email": email,
        "exp": expiration
    }
    token = jwt.encode(donnees, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decoder_token(token: str) -> dict:
    try:
        infos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return infos
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

def find_user_by_email(email: str, session: Session):
    requete = select(User).where(User.email == email)
    user = session.exec(requete).first()
    return user

def find_user_by_id(user_id: str, session: Session):
    user = session.get(User, user_id)
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    infos = decoder_token(token)
    user_id = infos.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    
    user = find_user_by_id(user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé"
        )
    
    return user



def validate_password(password: str):
    
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins 8 caractères"
        )
    
    if not any(c.isupper() for c in password):
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins une majuscule"
        )
    
    if not any(c.islower() for c in password):
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins une minuscule"
        )
    
    if not any(c.isdigit() for c in password):
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins un chiffre"
        )
    
    caracteres_speciaux = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
    if not any(c in caracteres_speciaux for c in password):
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins un caractère spécial (!@#$%...)"
        )


def validate_pseudo(pseudo: str):
    
    if len(pseudo) < 3:
        raise HTTPException(
            status_code=400,
            detail="Le pseudo doit contenir au moins 3 caractères"
        )
    
    if len(pseudo) > 20:
        raise HTTPException(
            status_code=400,
            detail="Le pseudo ne peut pas dépasser 20 caractères"
        )
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', pseudo):
        raise HTTPException(
            status_code=400,
            detail="Le pseudo ne peut contenir que des lettres, chiffres, _ et -"
        )


def validate_nom(nom: str, champ: str):
    
    if len(nom) < 2:
        raise HTTPException(
            status_code=400,
            detail=f"Le {champ} doit contenir au moins 2 caractères"
        )
    
    if not re.match(r'^[a-zA-ZÀ-ÿ\s-]+$', nom):
        raise HTTPException(
            status_code=400,
            detail=f"Le {champ} ne peut contenir que des lettres, espaces et tirets"
        )


def validate_age(age: int):
    
    if age < 18:
        raise HTTPException(
            status_code=400,
            detail="Vous devez avoir au moins 18 ans pour vous inscrire"
        )
    
    if age > 120:
        raise HTTPException(
            status_code=400,
            detail="L'âge semble incorrect"
        )


def validate_region(region: str):
    
    regions_valides = ["Europe", "America", "Asia", "Africa", "Oceania"]
    
    if region not in regions_valides:
        raise HTTPException(
            status_code=400,
            detail=f"La région doit être parmi: {', '.join(regions_valides)}"
        )


def validate_gender(gender: str):
    
    genders_valides = ["male", "female"]
    
    if gender not in genders_valides:
        raise HTTPException(
            status_code=400,
            detail=f"Le genre doit être parmi: {', '.join(genders_valides)}"
        )