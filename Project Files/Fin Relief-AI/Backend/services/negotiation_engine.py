"""
AI Negotiation Strategy Generator
----------------------------------
Tries Google Gemini first for a natural-language negotiation strategy and
letter. If Gemini is unavailable (no key / network error / quota), falls
back to a deterministic, template-based generator so the feature never
breaks in a demo or offline environment.
"""
from services.gemini_service import generate_content, GeminiUnavailableError


def generate_negotiation(
    user_name: str,
    lender_name: str,
    loan_type: str,
    outstanding_amount: float,
    overdue_months: int,
    suggested_settlement_pct: float,
    predicted_amount: float,
    stress_level: str,
    tone: str = "professional",
) -> dict:
    prompt = f"""You are a financial advisor AI helping a borrower negotiate debt settlement.

Borrower: {user_name}
Lender: {lender_name}
Loan type: {loan_type}
Outstanding amount: ₹{outstanding_amount:,.2f}
Overdue months: {overdue_months}
Financial stress level: {stress_level}
Suggested settlement: {suggested_settlement_pct}% (₹{predicted_amount:,.2f})
Requested tone: {tone}

Produce two things clearly labeled:
1. NEGOTIATION STRATEGY: 3-4 short bullet points of tactical advice for the borrower.
2. NEGOTIATION LETTER: A formal settlement request letter/email addressed to the lender,
   referencing the outstanding amount and proposing the settlement figure, written in a
   {tone} tone, no more than 200 words.
"""

    try:
        text = generate_content(prompt)
        strategy, letter = _split_ai_output(text)
        return {"strategy": strategy, "letter": letter, "source": "gemini"}
    except GeminiUnavailableError:
        return _rule_based_fallback(
            user_name, lender_name, loan_type, outstanding_amount,
            overdue_months, suggested_settlement_pct, predicted_amount,
            stress_level, tone,
        )


def _split_ai_output(text: str) -> tuple:
    """Best-effort split of Gemini's response into strategy + letter sections."""
    upper = text.upper()
    letter_idx = upper.find("NEGOTIATION LETTER")
    if letter_idx == -1:
        # Couldn't find a clean split - return whole thing as letter, generic strategy note
        return "AI-generated strategy included within the letter content below.", text.strip()

    strategy_part = text[:letter_idx].replace("NEGOTIATION STRATEGY", "").replace("1.", "").strip(" :\n1.")
    letter_part = text[letter_idx:].replace("NEGOTIATION LETTER", "").strip(" :\n2.")
    return strategy_part.strip(), letter_part.strip()


def _rule_based_fallback(
    user_name, lender_name, loan_type, outstanding_amount,
    overdue_months, suggested_settlement_pct, predicted_amount,
    stress_level, tone,
) -> dict:
    strategy_points = [
        f"Open with a lump-sum offer near ₹{predicted_amount:,.0f} ({suggested_settlement_pct}% of outstanding) "
        f"since the account has been overdue for {overdue_months} month(s).",
        "Reference documented financial hardship (income vs. expenses) to justify the reduced offer.",
        "Request a written 'settled in full' confirmation before making any payment.",
        "If rejected, propose a short structured payment plan as a fallback instead of a lump sum.",
    ]
    if stress_level in ("High", "Critical"):
        strategy_points.append(
            "Mention potential hardship/legal-aid support if needed, since financial stress is currently "
            f"rated '{stress_level}', to encourage lender flexibility."
        )
    strategy = "\n".join(f"- {p}" for p in strategy_points)

    tone_opening = {
        "professional": "I am writing to formally propose a settlement",
        "firm": "I am writing to state clearly my proposed settlement terms",
        "empathetic": "I am reaching out in good faith to discuss a settlement",
    }.get(tone, "I am writing to formally propose a settlement")

    letter = f"""Subject: Settlement Proposal for {loan_type} Account – {user_name}

Dear {lender_name} Team,

{tone_opening} regarding my outstanding {loan_type.lower()} balance of ₹{outstanding_amount:,.2f}, which is currently {overdue_months} month(s) overdue.

Due to ongoing financial constraints, I am unable to repay the full outstanding amount at this time. However, I am able to arrange a one-time settlement payment of ₹{predicted_amount:,.2f} (approximately {suggested_settlement_pct}% of the outstanding balance), payable promptly upon written agreement.

I kindly request that this be treated as a full and final settlement of the account, with confirmation provided in writing before payment is made, and the account subsequently reported as "settled" to credit bureaus.

I appreciate your understanding and look forward to resolving this matter amicably.

Sincerely,
{user_name}
"""
    return {"strategy": strategy, "letter": letter.strip(), "source": "rule-based-fallback"}
