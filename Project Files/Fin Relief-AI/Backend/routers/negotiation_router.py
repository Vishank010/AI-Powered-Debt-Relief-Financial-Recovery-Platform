from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import get_current_user
from services.financial_engine import calculate_financial_profile
from services.settlement_engine import predict_settlement
from services.negotiation_engine import generate_negotiation

router = APIRouter(prefix="/api/negotiation", tags=["AI Negotiation"])


@router.post("/generate", response_model=schemas.NegotiationOut, status_code=201)
def generate(payload: schemas.NegotiationRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == payload.LoanID, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    all_loans = db.query(models.Loan).filter(models.Loan.UserID == current_user.UserID).all()
    profile_calc = calculate_financial_profile(current_user.MonthlyIncome, current_user.MonthlyExpenses, all_loans)
    settlement_calc = predict_settlement(
        outstanding_amount=loan.OutstandingAmount,
        overdue_months=loan.OverdueMonths,
        interest_rate=loan.InterestRate,
        stress_level=profile_calc["StressLevel"],
    )

    ai_result = generate_negotiation(
        user_name=current_user.Name,
        lender_name=loan.LenderName,
        loan_type=loan.LoanType,
        outstanding_amount=loan.OutstandingAmount,
        overdue_months=loan.OverdueMonths,
        suggested_settlement_pct=settlement_calc["SuggestedSettlement"],
        predicted_amount=settlement_calc["PredictedAmount"],
        stress_level=profile_calc["StressLevel"],
        tone=payload.Tone,
    )

    negotiation = models.AINegotiation(
        LoanID=loan.LoanID,
        UserID=current_user.UserID,
        NegotiationStrategy=ai_result["strategy"],
        NegotiationLetter=ai_result["letter"],
    )
    db.add(negotiation)

    history = models.AIHistory(
        UserID=current_user.UserID,
        GeneratedContent=f"Negotiation letter generated for {loan.LenderName} (source: {ai_result['source']})",
        QueryType="negotiation",
    )
    db.add(history)
    db.commit()
    db.refresh(negotiation)
    return negotiation


@router.get("/loan/{loan_id}", response_model=List[schemas.NegotiationOut])
def get_negotiations_for_loan(loan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    loan = db.query(models.Loan).filter(models.Loan.LoanID == loan_id, models.Loan.UserID == current_user.UserID).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db.query(models.AINegotiation).filter(models.AINegotiation.LoanID == loan_id).order_by(models.AINegotiation.GeneratedDate.desc()).all()
