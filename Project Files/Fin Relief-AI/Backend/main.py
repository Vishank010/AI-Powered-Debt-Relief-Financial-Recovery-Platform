from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import auth_router, loans_router, financial_router, settlement_router, negotiation_router, history_router

# Create all tables on startup (SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinRelief AI - Debt Relief & Financial Recovery Platform",
    description="AI powered API for financial health analysis, settlement prediction, and negotiation letter generation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(loans_router.router)
app.include_router(financial_router.router)
app.include_router(settlement_router.router)
app.include_router(negotiation_router.router)
app.include_router(history_router.router)


@app.get("/")
def root():
    return {"message": "FinRelief AI API is running", "docs": "/docs"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
