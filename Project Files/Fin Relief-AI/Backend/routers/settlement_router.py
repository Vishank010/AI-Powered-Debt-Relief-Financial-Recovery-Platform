from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import get_current_user
from services.financial_engine import calculate_financial_profile
from services.settlement_engine import predict_settlement

router = APIRouter(prefix="/api/settlement", tags=["Settlement Prediction"])


@router.post("/predict/{loan_id}", response_model=schemas.SettlementPredictionOut, status_code=201)
def predict(loan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == loan_id, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    all_loans = db.query(models.Loan).filter(models.Loan.UserID == current_user.UserID).all()
    profile_calc = calculate_financial_profile(current_user.MonthlyIncome, current_user.MonthlyExpenses, all_loans)

    result = predict_settlement(
        outstanding_amount=loan.OutstandingAmount,
        overdue_months=loan.OverdueMonths,
        interest_rate=loan.InterestRate,
        stress_level=profile_calc["StressLevel"],
    )

    prediction = models.SettlementPrediction(LoanID=loan.LoanID, **result)
    db.add(prediction)

    history = models.AIHistory(
        UserID=current_user.UserID,
        GeneratedContent=f"Settlement prediction for {loan.LenderName} ({loan.LoanType}): "
                          f"{result['SuggestedSettlement']}% -> ₹{result['PredictedAmount']}, risk: {result['RiskCategory']}",
        QueryType="settlement",
    )
    db.add(history)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/loan/{loan_id}", response_model=List[schemas.SettlementPredictionOut])
def get_predictions_for_loan(loan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == loan_id, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db.query(models.SettlementPrediction).filter(models.SettlementPrediction.LoanID == loan_id).order_by(models.SettlementPrediction.CreatedAt.desc()).all()
