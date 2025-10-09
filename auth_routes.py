from fastapi import APIRouter, Depends, HTTPException, status
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

router = APIRouter(prefix="/auth", tags=["Authentification"])

SECRET_KEY = "change_moi_en_production_123456"
ALGORITHM = "HS256"
ph = PasswordHasher()
bearer = HTTPBearer()


class InscriptionData(BaseModel):
    pseudo: str
    name: str
    firstname: str
    password: str
    email: EmailStr
    age: int
    region: str
    gender: str

class ConnexionData(BaseModel):
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
    
    class Config:
        from_attributes = True


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

def trouver_user_par_email(email: str, session: Session):
    requete = select(User).where(User.email == email)
    user = session.exec(requete).first()
    return user

def trouver_user_par_id(user_id: str, session: Session):
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
    
    user = trouver_user_par_id(user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé"
        )
    
    return user


@router.post("/inscription", response_model=UserResponse, status_code=201)
def inscription(
    data: InscriptionData,
    session: Session = Depends(get_session)
):
    
    # 1. Vérifier si l'email existe déjà
    user_existe = trouver_user_par_email(data.email, session)
    if user_existe:
        raise HTTPException(
            status_code=400,
            detail="Cet email est déjà utilisé"
        )
    
    if data.age < 18:
        raise HTTPException(
            status_code=400,
            detail="Vous devez avoir au moins 18 ans pour ouvrir un compte bancaire."
    )
    
    password_hashe = hasher_password(data.password)
    
    nouveau_user = create_user(
        pseudo=data.pseudo,
        name=data.name,
        firstname=data.firstname,
        password=password_hashe,
        email=data.email,
        age=data.age,
        region=data.region,
        gender=data.gender,
        session=session
    )

    session.add(nouveau_user)
    session.commit()
    session.refresh(nouveau_user)
    
    return nouveau_user


@router.post("/connexion")
def connexion(
    data: ConnexionData,
    session: Session = Depends(get_session)
):
    user = trouver_user_par_email(data.email, session)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )
    
    password_correct = verifier_password(user.hashed_password, data.password)
    
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


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user