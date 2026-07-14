# FinRelief AI – Debt Relief & Financial Recovery Platform

An AI-powered web application that helps borrowers manage loans, analyze
financial health, get AI-driven settlement predictions, and generate
lender-specific negotiation letters using Google Gemini.

**Stack:** React.js (Vite + Tailwind) · FastAPI · SQLite · SQLAlchemy · Google Gemini API

---

## 1. Project Structure

```
finrelief-ai/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── database.py              # SQLAlchemy engine/session
│   ├── models.py                # DB models (matches ER diagram)
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── auth.py                   # JWT auth + password hashing
│   ├── requirements.txt
│   ├── .env.example
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── loans_router.py
│   │   ├── financial_router.py
│   │   ├── settlement_router.py
│   │   ├── negotiation_router.py
│   │   └── history_router.py
│   └── services/
│       ├── financial_engine.py       # EMI/DTI/stress calculations
│       ├── settlement_engine.py      # Settlement % prediction
│       ├── gemini_service.py         # Google Gemini API wrapper
│       └── negotiation_engine.py     # AI letter generator + fallback
└── frontend/
    ├── src/
    │   ├── pages/            # Login, Register, Dashboard, Loans, Settlement, Negotiation, History
    │   ├── components/       # Navbar, StatCard, ProtectedRoute
    │   ├── context/          # AuthContext (JWT + user state)
    │   └── api/client.js     # Axios instance with auth interceptor
    ├── package.json
    └── vite.config.js
```

This maps directly onto the ER diagram: **Users → Financial_Profile / Loans /
AI_History**, and **Loans → Settlement_Prediction / AI_Negotiation**.

---

## 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then edit .env with your values
```

Edit `.env`:
- `SECRET_KEY` — any long random string (used to sign JWTs)
- `GEMINI_API_KEY` — get a free key at https://aistudio.google.com/app/apikey
  (optional — if left blank, the app automatically uses rule-based
  negotiation letters instead of calling Gemini)

Run the server:
```bash
uvicorn main:app --reload --port 8000
```

API docs will be available at **http://localhost:8000/docs** (Swagger UI).

The SQLite database file (`finrelief.db`) and all tables are created
automatically on first run.

---

## 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App runs at **http://localhost:5173**. Vite is configured to proxy `/api`
requests to `http://localhost:8000`, so the backend must be running first.

---

## 4. How It Works

### Financial Health Engine (rule-based, deterministic)
- **EMI Ratio** = total monthly EMI ÷ monthly income
- **DTI Ratio** = (total EMI + other expenses) ÷ monthly income
- **Monthly Surplus** = income − expenses − EMI
- **Stress Level** = weighted score from DTI ratio, surplus, and overdue months
  → Low / Moderate / High / Critical

### Settlement Prediction Engine (rule-based)
Starts from an 80% base settlement offer and discounts it based on overdue
months, stress level, and interest rate, producing a suggested settlement
percentage, risk category, and predicted payoff amount.

### AI Negotiation Letter Generator
Tries **Google Gemini** (`gemini-1.5-flash`) first to generate a natural
negotiation strategy + letter. If no API key is set, or the Gemini call
fails for any reason (network, quota, etc.), it automatically falls back
to a template-based generator — so the feature always works, even offline
or during a live demo.

### Auth
JWT-based authentication with bcrypt-hashed passwords via `python-jose` +
`passlib`. Tokens are stored in `localStorage` on the frontend and attached
to every API request via an Axios interceptor.

---

## 5. API Endpoints (summary)

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|-------------------------------------|
| POST   | `/api/auth/register`              | Create account, returns JWT         |
| POST   | `/api/auth/login`                 | Login, returns JWT                  |
| GET    | `/api/auth/me`                    | Current user profile                |
| PUT    | `/api/auth/me/income`             | Update income/expenses              |
| GET/POST/PUT/DELETE | `/api/loans/`        | Loan CRUD                           |
| GET    | `/api/financial/profile`          | Financial health metrics            |
| POST   | `/api/settlement/predict/{loan_id}` | Run settlement prediction         |
| GET    | `/api/settlement/loan/{loan_id}`  | Prediction history for a loan       |
| POST   | `/api/negotiation/generate`       | Generate negotiation strategy+letter|
| GET    | `/api/negotiation/loan/{loan_id}` | Negotiation history for a loan      |
| GET    | `/api/history/`                   | Full AI activity history            |

Full interactive documentation is auto-generated at `/docs`.

---

## 6. Notes for Submission

- The ER diagram in your project brief is fully implemented in `models.py`
  (`Users`, `Financial_Profile`, `Loans`, `Settlement_Prediction`,
  `AI_Negotiation`, `AI_History`) with correct 1:1 / 1:N relationships.
- The enterprise architecture (User Layer → Frontend → API Layer → AI &
  Financial Processing Layer → Database Layer) is reflected in the folder
  structure: routers = API layer, services = AI/financial processing layer.
- No network access was available in this environment to run `npm install`
  or `pip install` live, so please run the install commands above locally
  before starting the servers. All code has been syntax-validated.
