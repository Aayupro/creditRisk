from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.db import get_db
from utils.auth_utils import get_current_user
from feature_engineering.engine import FeatureEngine
from rule_engine.risk_rules import RuleBasedRiskEngine
from ml_models.pipeline import ml_pipeline
import json
from datetime import datetime

router = APIRouter()

class LoanSchema(BaseModel):
    full_name: str; age: int; gender: str; occupation: str; annual_income: float; monthly_income: float
    existing_loans: int; existing_emis: float; loan_amount: float; loan_purpose: str; loan_tenure: int
    employment_type: str; years_of_employment: float; credit_score: int; dependents: int; assets: float; liabilities: float

@router.post("/apply")
def apply(data: LoanSchema, user: dict = Depends(get_current_user)):
    feat = FeatureEngine.compute_all(data.dict())
    r_score, details = RuleBasedRiskEngine.evaluate(data.dict(), feat)
    
    vec = [data.age, data.annual_income, data.loan_amount, data.loan_tenure, data.credit_score, feat['dti'], feat['lti'], feat['emi_burden'], feat['disposable_income'], feat['emp_stability']]
    prob = ml_pipeline.predict_risk(vec)
    
    comp = (100 - r_score) * 0.4 + (prob * 100) * 0.6
    cat, dec = ("Very Low Risk", "Approved") if comp < 20 else ("Low Risk", "Approved") if comp < 40 else ("Medium Risk", "Manual Review") if comp < 60 else ("High Risk", "Conditionally Approved") if comp < 80 else ("Very High Risk", "Rejected")
    
    conn = next(get_db())
    cursor = conn.cursor()
    cursor.execute("'''INSERT INTO applications (user_id, full_name, age, gender, occupation, annual_income, monthly_income, existing_loans, existing_emis, loan_amount, loan_purpose, loan_tenure, employment_type, years_of_employment, credit_score, dependents, assets, liabilities, status, rule_score, ml_prob, risk_category, decision, explanation, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''",
                   (user['sub'], data.full_name, data.age, data.gender, data.occupation, data.annual_income, data.monthly_income, data.existing_loans, data.existing_emis, data.loan_amount, data.loan_purpose, data.loan_tenure, data.employment_type, data.years_of_employment, data.credit_score, data.dependents, data.assets, data.liabilities, dec, r_score, prob, cat, dec, json.dumps({"deductions": details, "metrics": feat}), datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    return {"decision": dec}

@router.get("/history")
def history(user: dict = Depends(get_current_user)):
    conn = next(get_db())
    cursor = conn.cursor()
    if user['role'] == 'officer':
        cursor.execute("SELECT * FROM applications ORDER BY id DESC")
    else:
        cursor.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY id DESC", (user['sub'],))
    return [dict(r) for r in cursor.fetchall()]