from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/loans", tags=["Loans"])


@router.post("/", response_model=schemas.LoanOut, status_code=201)
def create_loan(payload: schemas.LoanCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = models.Loan(UserID=current_user.UserID, **payload.model_dump())
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@router.get("/", response_model=List[schemas.LoanOut])
def list_loans(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Loan).filter(models.Loan.UserID == current_user.UserID).all()


@router.get("/{loan_id}", response_model=schemas.LoanOut)
def get_loan(loan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == loan_id, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.put("/{loan_id}", response_model=schemas.LoanOut)
def update_loan(loan_id: int, payload: schemas.LoanCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == loan_id, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    for key, value in payload.model_dump().items():
        setattr(loan, key, value)
    db.commit()
    db.refresh(loan)
    return loan


@router.delete("/{loan_id}", status_code=204)
def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == loan_id, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(loan)
    db.commit()
    return None
