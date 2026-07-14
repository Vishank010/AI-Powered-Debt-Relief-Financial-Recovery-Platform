from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["AI History"])


@router.get("/", response_model=List[schemas.AIHistoryOut])
def get_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return (
        db.query(models.AIHistory)
        .filter(models.AIHistory.UserID == current_user.UserID)
        .order_by(models.AIHistory.Timestamp.desc())
        .all()
    )
