from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET = os.getenv('AUTH_SECRET', 'VerySecretChangeMe123!')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'sub': username, 'exp': expire.timestamp()}
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get('sub')
    except Exception:
        return None

@router.post('/register', response_model=schemas.UserRead)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail='username already exists')
    hashed = bcrypt.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post('/login', response_model=schemas.TokenResponse)
def login(form: dict, db: Session = Depends(get_db)):
    username = form.get('username')
    password = form.get('password')
    if not username or not password:
        raise HTTPException(status_code=400, detail='username and password required')
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user or not bcrypt.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid credentials')
    token = create_token(db_user.username)
    return {'access_token': token, 'token_type': 'bearer'}
