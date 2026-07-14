from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import get_current_user
from services.financial_engine import calculate_financial_profile

router = APIRouter(prefix="/api/financial", tags=["Financial Health"])


@router.get("/profile", response_model=schemas.FinancialProfileOut)
def get_financial_profile(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loans = db.query(models.Loan).filter(models.Loan.UserID == current_user.UserID).all()
    result = calculate_financial_profile(current_user.MonthlyIncome, current_user.MonthlyExpenses, loans)

    profile = db.query(models.FinancialProfile).filter(models.FinancialProfile.UserID == current_user.UserID).first()
    if not profile:
        profile = models.FinancialProfile(UserID=current_user.UserID)
        db.add(profile)

    profile.EMI_Ratio = result["EMI_Ratio"]
    profile.DTI_Ratio = result["DTI_Ratio"]
    profile.MonthlySurplus = result["MonthlySurplus"]
    profile.StressLevel = result["StressLevel"]
    db.commit()
    db.refresh(profile)
    return profile
