"""
Settlement Prediction Engine
-----------------------------
Rule-based model that suggests a settlement percentage (of the outstanding
loan amount) based on overdue duration, interest rate, and the borrower's
overall financial stress. This mimics what a trained ML model would output,
using a transparent, explainable scoring formula.
"""


def predict_settlement(outstanding_amount: float, overdue_months: int, interest_rate: float, stress_level: str) -> dict:
    # Base settlement starts high (lender wants more) and decreases as
    # overdue months / stress increases (lender more willing to settle for less)
    base_percentage = 80.0

    # Overdue impact - longer overdue = lender accepts lower settlement
    overdue_discount = min(overdue_months * 2.5, 35)

    # Stress level impact
    stress_discount_map = {
        "Low": 0,
        "Moderate": 5,
        "High": 10,
        "Critical": 18,
    }
    stress_discount = stress_discount_map.get(stress_level, 0)

    # High interest loans (e.g. credit cards) tend to allow bigger settlement cuts
    interest_discount = 5 if interest_rate >= 24 else (2 if interest_rate >= 15 else 0)

    suggested_percentage = base_percentage - overdue_discount - stress_discount - interest_discount
    suggested_percentage = max(35.0, min(95.0, suggested_percentage))  # clamp between 35% - 95%

    predicted_amount = round(outstanding_amount * (suggested_percentage / 100), 2)

    # Risk category for the lender's perspective on recovering this debt
    risk_score = overdue_months + (10 if stress_level in ("High", "Critical") else 0)
    if risk_score >= 15:
        risk_category = "High"
    elif risk_score >= 6:
        risk_category = "Medium"
    else:
        risk_category = "Low"

    return {
        "SuggestedSettlement": round(suggested_percentage, 2),
        "RiskCategory": risk_category,
        "PredictedAmount": predicted_amount,
    }
