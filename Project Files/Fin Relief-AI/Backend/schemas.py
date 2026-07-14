from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ---------- Auth / Users ----------
class UserCreate(BaseModel):
    Name: str
    Email: EmailStr
    Password: str
    MonthlyIncome: float = 0.0
    MonthlyExpenses: float = 0.0


class UserLogin(BaseModel):
    Email: EmailStr
    Password: str


class UserOut(BaseModel):
    UserID: int
    Name: str
    Email: EmailStr
    MonthlyIncome: float
    MonthlyExpenses: float

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserUpdateIncome(BaseModel):
    MonthlyIncome: float
    MonthlyExpenses: float


# ---------- Financial Profile ----------
class FinancialProfileOut(BaseModel):
    ProfileID: int
    UserID: int
    EMI_Ratio: float
    DTI_Ratio: float
    MonthlySurplus: float
    StressLevel: str

    class Config:
        from_attributes = True


# ---------- Loans ----------
class LoanCreate(BaseModel):
    LenderName: str
    LoanType: str
    OutstandingAmount: float
    InterestRate: float
    EMI: float
    OverdueMonths: int = 0


class LoanOut(BaseModel):
    LoanID: int
    UserID: int
    LenderName: str
    LoanType: str
    OutstandingAmount: float
    InterestRate: float
    EMI: float
    OverdueMonths: int

    class Config:
        from_attributes = True


# ---------- Settlement Prediction ----------
class SettlementPredictionOut(BaseModel):
    SettlementID: int
    LoanID: int
    SuggestedSettlement: float
    RiskCategory: str
    PredictedAmount: float
    CreatedAt: datetime

    class Config:
        from_attributes = True


# ---------- AI Negotiation ----------
class NegotiationRequest(BaseModel):
    LoanID: int
    Tone: Optional[str] = "professional"  # professional / firm / empathetic


class NegotiationOut(BaseModel):
    AI_ID: int
    LoanID: int
    UserID: int
    NegotiationStrategy: str
    NegotiationLetter: str
    GeneratedDate: datetime

    class Config:
        from_attributes = True


# ---------- AI History ----------
class AIHistoryOut(BaseModel):
    HistoryID: int
    UserID: int
    GeneratedContent: str
    QueryType: str
    Timestamp: datetime

    class Config:
        from_attributes = True
