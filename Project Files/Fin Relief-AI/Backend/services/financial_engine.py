"""
Financial Health Engine
------------------------
Pure rule-based calculations for EMI ratio, DTI ratio, monthly surplus,
and overall debt stress level. No external API calls are needed here -
this is deterministic financial math.
"""
from typing import List


def calculate_financial_profile(monthly_income: float, monthly_expenses: float, loans: List) -> dict:
    total_emi = sum(loan.EMI for loan in loans) if loans else 0.0

    # EMI Ratio = total EMI obligations / monthly income
    emi_ratio = round((total_emi / monthly_income) * 100, 2) if monthly_income > 0 else 0.0

    # DTI Ratio (Debt-to-Income) = (EMI + other fixed expenses) / income
    dti_ratio = round(((total_emi + monthly_expenses) / monthly_income) * 100, 2) if monthly_income > 0 else 0.0

    # Monthly Surplus = income - expenses - EMI
    monthly_surplus = round(monthly_income - monthly_expenses - total_emi, 2)

    # Overdue-weighted stress
    max_overdue = max((loan.OverdueMonths for loan in loans), default=0)

    stress_level = _determine_stress_level(dti_ratio, monthly_surplus, max_overdue)

    return {
        "EMI_Ratio": emi_ratio,
        "DTI_Ratio": dti_ratio,
        "MonthlySurplus": monthly_surplus,
        "StressLevel": stress_level,
    }


def _determine_stress_level(dti_ratio: float, monthly_surplus: float, max_overdue: int) -> str:
    score = 0

    if dti_ratio >= 70:
        score += 3
    elif dti_ratio >= 50:
        score += 2
    elif dti_ratio >= 35:
        score += 1

    if monthly_surplus < 0:
        score += 3
    elif monthly_surplus < 2000:
        score += 1

    if max_overdue >= 6:
        score += 3
    elif max_overdue >= 3:
        score += 2
    elif max_overdue >= 1:
        score += 1

    if score >= 6:
        return "Critical"
    elif score >= 4:
        return "High"
    elif score >= 2:
        return "Moderate"
    return "Low"
