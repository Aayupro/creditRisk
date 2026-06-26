from fastapi import APIRouter, Depends
from database.db import get_db
from utils.auth_utils import get_current_user

router = APIRouter()

@router.get("/summary")
def summary(user: dict = Depends(get_current_user)):
    conn = next(get_db())
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN decision IN ('Approved','Conditionally Approved') THEN 1 ELSE 0 END), AVG(rule_score), AVG(loan_amount) FROM applications")
    stats = cursor.fetchone()
    return {
        "total_applications": stats[0] or 0,
        "approved_loans": stats[1] or 0,
        "avg_risk_score": round(stats[2] or 0, 2),
        "avg_loan_amount": round(stats[3] or 0, 2)
    }