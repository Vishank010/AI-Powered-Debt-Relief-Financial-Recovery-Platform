from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    UserID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Email = Column(String, unique=True, index=True, nullable=False)
    Password = Column(String, nullable=False)  # stored as bcrypt hash
    MonthlyIncome = Column(Float, default=0.0)
    MonthlyExpenses = Column(Float, default=0.0)

    financial_profile = relationship("FinancialProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    ai_history = relationship("AIHistory", back_populates="user", cascade="all, delete-orphan")


class FinancialProfile(Base):
    __tablename__ = "financial_profile"

    ProfileID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False, unique=True)
    EMI_Ratio = Column(Float, default=0.0)
    DTI_Ratio = Column(Float, default=0.0)
    MonthlySurplus = Column(Float, default=0.0)
    StressLevel = Column(String, default="Low")  # Low / Moderate / High / Critical

    user = relationship("User", back_populates="financial_profile")


class Loan(Base):
    __tablename__ = "loans"

    LoanID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    LenderName = Column(String, nullable=False)
    LoanType = Column(String, nullable=False)  # Personal / Credit Card / Auto / Home / Other
    OutstandingAmount = Column(Float, nullable=False)
    InterestRate = Column(Float, nullable=False)
    EMI = Column(Float, nullable=False)
    OverdueMonths = Column(Integer, default=0)

    user = relationship("User", back_populates="loans")
    settlement_predictions = relationship("SettlementPrediction", back_populates="loan", cascade="all, delete-orphan")
    negotiations = relationship("AINegotiation", back_populates="loan", cascade="all, delete-orphan")


class SettlementPrediction(Base):
    __tablename__ = "settlement_prediction"

    SettlementID = Column(Integer, primary_key=True, index=True)
    LoanID = Column(Integer, ForeignKey("loans.LoanID"), nullable=False)
    SuggestedSettlement = Column(Float, nullable=False)  # % of outstanding amount
    RiskCategory = Column(String, nullable=False)  # Low / Medium / High
    PredictedAmount = Column(Float, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    loan = relationship("Loan", back_populates="settlement_predictions")


class AINegotiation(Base):
    __tablename__ = "ai_negotiation"

    AI_ID = Column(Integer, primary_key=True, index=True)
    LoanID = Column(Integer, ForeignKey("loans.LoanID"), nullable=False)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    NegotiationStrategy = Column(Text, nullable=False)
    NegotiationLetter = Column(Text, nullable=False)
    GeneratedDate = Column(DateTime, default=datetime.utcnow)

    loan = relationship("Loan", back_populates="negotiations")


class AIHistory(Base):
    __tablename__ = "ai_history"

    HistoryID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    GeneratedContent = Column(Text, nullable=False)
    QueryType = Column(String, nullable=False)  # settlement / negotiation
    Timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ai_history")
