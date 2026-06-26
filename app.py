import os
import sqlite3
import jwt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import json

DB_NAME = "credit_risk_engine.db"
SECRET_KEY = "SUPER_SECRET_FINTECH_KEY_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Baseline Structural Models State
class MLState:
    def __init__(self):
        self.features = ['age', 'annual_income', 'loan_amount', 'loan_tenure', 'credit_score', 'dti', 'lti', 'emi_burden', 'disposable_income', 'emp_stability']
    
    def predict_risk(self, vector: list) -> float:
        # Balanced linear heuristic estimator for mock simulation 
        scr = vector[4]
        dti = vector[5]
        prob = 0.1
        if scr < 600: prob += 0.5
        if dti > 0.45: prob += 0.3
        return min(0.99, max(0.01, prob))

ml_state = MLState()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT, role TEXT, full_name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, full_name TEXT, age INTEGER, gender TEXT, occupation TEXT, annual_income REAL, monthly_income REAL, existing_loans INTEGER, existing_emis REAL, loan_amount REAL, loan_purpose TEXT, loan_tenure INTEGER, employment_type TEXT, years_of_employment REAL, credit_score INTEGER, dependents INTEGER, assets REAL, liabilities REAL, status TEXT, rule_score REAL, ml_prob REAL, risk_category TEXT, decision TEXT, explanation TEXT, created_at TEXT)")
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

class UserLogin(BaseModel):
    email: str
    password: str

class LoanSchema(BaseModel):
    full_name: str; age: int; gender: str; occupation: str; annual_income: float; monthly_income: float
    existing_loans: int; existing_emis: float; loan_amount: float; loan_purpose: str; loan_tenure: int
    employment_type: str; years_of_employment: float; credit_score: int; dependents: int; assets: float; liabilities: float

@app.post("/api/auth/login")
def login(data: UserLogin):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (data.email,))
    user = c.fetchone()
    conn.close()
    return {"access_token": "MOCK_TOKEN", "role": user['role'] if user else ("officer" if "officer" in data.email else "customer"), "name": data.email.split('@')[0]}

@app.post("/api/loans/apply")
def apply(data: LoanSchema):
    annual_income = max(1.0, data.annual_income)
    monthly_income = max(1.0, data.monthly_income)
    new_emi = data.loan_amount / max(1, data.loan_tenure)
    total_emi = data.existing_emis + new_emi
    
    # Feature Calculations
    dti = (total_emi * 12) / annual_income
    lti = data.loan_amount / annual_income
    emi_burden = total_emi / monthly_income
    disposable = monthly_income - total_emi - (data.dependents * 200)
    emp_stability = min((data.years_of_employment / 4.0) * 100, 100.0)
    
    # Rule Evaluation Matrix
    r_score = 100.0
    details = []
    if dti > 0.45: r_score -= 25; details.append("High Debt-to-Income ratio (>45%)")
    if emi_burden > 0.50: r_score -= 20; details.append("Critical Monthly EMI Burden (>50%)")
    if data.credit_score < 600: r_score -= 30; details.append("Poor Credit Score (<600)")
    
    vec = [data.age, data.annual_income, data.loan_amount, data.loan_tenure, data.credit_score, dti, lti, emi_burden, disposable, emp_stability]
    prob = ml_state.predict_risk(vec)
    
    comp = (100 - r_score) * 0.4 + (prob * 100) * 0.6
    cat, dec = ("Low Risk", "Approved") if comp < 40 else ("Medium Risk", "Manual Review") if comp < 60 else ("High Risk", "Rejected")
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO applications (full_name, age, gender, occupation, annual_income, monthly_income, existing_loans, existing_emis, loan_amount, loan_purpose, loan_tenure, employment_type, years_of_employment, credit_score, dependents, assets, liabilities, status, rule_score, ml_prob, risk_category, decision, explanation, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (data.full_name, data.age, data.gender, data.occupation, data.annual_income, data.monthly_income, data.existing_loans, data.existing_emis, data.loan_amount, data.loan_purpose, data.loan_tenure, data.employment_type, data.years_of_employment, data.credit_score, data.dependents, data.assets, data.liabilities, dec, r_score, prob, cat, dec, json.dumps({"deductions": details, "metrics": {"dti": dti, "disposable_income": disposable}}), datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
    return {"decision": dec}

@app.get("/api/loans/history")
def history():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM applications ORDER BY id DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

@app.get("/api/analytics/summary")
def summary():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(CASE WHEN decision='Approved' THEN 1 ELSE 0 END), AVG(rule_score), AVG(loan_amount) FROM applications")
    stats = c.fetchone()
    conn.close()
    return {"total_applications": stats[0] or 0, "approved_loans": stats[1] or 0, "avg_risk_score": round(stats[2] or 0, 2), "avg_loan_amount": round(stats[3] or 0, 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)