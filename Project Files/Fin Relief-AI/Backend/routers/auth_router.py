from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.Email == payload.Email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        Name=payload.Name,
        Email=payload.Email,
        Password=hash_password(payload.Password),
        MonthlyIncome=payload.MonthlyIncome,
        MonthlyExpenses=payload.MonthlyExpenses,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize an empty financial profile for the new user
    profile = models.FinancialProfile(UserID=user.UserID)
    db.add(profile)
    db.commit()

    token = create_access_token({"sub": str(user.UserID)})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.Email == payload.Email).first()
    if not user or not verify_password(payload.Password, user.Password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.UserID)})
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me/income", response_model=schemas.UserOut)
def update_income(payload: schemas.UserUpdateIncome, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    current_user.MonthlyIncome = payload.MonthlyIncome
    current_user.MonthlyExpenses = payload.MonthlyExpenses
    db.commit()
    db.refresh(current_user)
    return current_user
