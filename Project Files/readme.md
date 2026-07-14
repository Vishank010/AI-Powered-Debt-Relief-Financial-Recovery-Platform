# Project Files – FinRelief AI

This folder contains the complete source code for the **AI Powered Debt Relief 
& Financial Recovery Platform**.

## Tech Stack
- **Frontend:** React.js (Vite) + Tailwind CSS
- **Backend:** FastAPI (Python)
- **Database:** SQLite + SQLAlchemy ORM
- **AI Integration:** Google Gemini API (with rule-based fallback)
- **Auth:** JWT-based authentication with bcrypt password hashing

## Folder Structure
backend/
├── main.py              # FastAPI entrypoint
├── models.py             # Database models (ER diagram)
├── schemas.py             # Pydantic request/response schemas
├── auth.py                # JWT auth + password hashing
├── routers/               # API endpoints (auth, loans, financial, settlement, negotiation, history)
└── services/              # Financial engine, settlement engine, Gemini integration, negotiation engine
frontend/
├── src/
│   ├── pages/             # Login, Register, Dashboard, Loans, Settlement, Negotiation, History
│   ├── components/        # Navbar, StatCard, ProtectedRoute
│   ├── context/           # AuthContext (JWT + user state)
│   └── api/client.js      # Axios instance with auth interceptor

## Key Features
- Secure user registration & login
- Loan management (add / edit / delete)
- Financial health engine (EMI ratio, DTI ratio, stress level)
- AI-driven settlement prediction with risk categorization
- AI negotiation strategy & letter generator (Gemini-powered, with fallback)
- Full AI activity history log

## Setup Instructions
See root `README.md` for complete step-by-step backend and frontend setup 
instructions (Python + Node.js required).
