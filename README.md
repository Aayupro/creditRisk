# 💳 Credit Risk & Loan Approval Engine

A high-performance, production-ready REST API that automates loan underwriting by combining rule-based compliance checks with machine learning probability scoring.

This repository implements a **weighted hybrid scoring engine**, automated feature engineering pipelines, secure role-based application workflows, and real-time risk analytics.

---

## 📌 Table of Contents

* [Overview](https://www.google.com/search?q=%23overview)
* [Key Features](https://www.google.com/search?q=%23key-features)
* [System Architecture & Workflow](https://www.google.com/search?q=%23system-architecture--workflow)
* [Tech Stack](https://www.google.com/search?q=%23tech-stack)
* [Project Structure](https://www.google.com/search?q=%23project-structure)
* [Getting Started](https://www.google.com/search?q=%23getting-started)
* [Prerequisites](https://www.google.com/search?q=%23prerequisites)
* [Installation](https://www.google.com/search?q=%23installation)
* [Environment Setup](https://www.google.com/search?q=%23environment-setup)


* [Usage](https://www.google.com/search?q=%23usage)
* [1. Database Migration & Setup](https://www.google.com/search?q=%231-database-migration--setup)
* [2. Model Training](https://www.google.com/search?q=%232-model-training)
* [3. Running the FastAPI Server](https://www.google.com/search?q=%233-running-the-fastapi-server)


* [API Reference](https://www.google.com/search?q=%23api-reference)
* [Hybrid Scoring Methodology](https://www.google.com/search?q=%23hybrid-scoring-methodology)
* [License](https://www.google.com/search?q=%23license)

---

## 🌟 Overview

Traditional credit scoring systems either rely solely on rigid rule-based logic or opaque black-box ML models. This project bridges that gap by using a **Weighted Hybrid Scorer**:

1. **Rule-Based Compliance Layer**: Enforces strict financial thresholds (e.g., maximum allowable Debt-to-Income, minimum disposable income, regulatory checks).
2. **Machine Learning Layer**: Evaluates historical applicant profiles using `scikit-learn` to estimate default probability.
3. **Decision Engine**: Blends compliance outputs and ML probability scores into an automated decision (`APPROVED`, `MANUAL_REVIEW`, or `REJECTED`).

---

## ✨ Key Features

* **Weighted Hybrid Scoring Engine**: Blends deterministic regulatory/policy rules with probabilistic machine learning predictions into a unified credit decision.
* **Automated Feature Engineering**: Transforms raw applicant financial inputs into key lending metrics:
* **DTI** (Debt-to-Income Ratio)
* **LTI** (Loan-to-Income Ratio)
* **EMI Burden** (Equated Monthly Installment Burden)
* **Disposable Income** (Net monthly liquid income after existing liabilities)


* **Role-Based Access Control (RBAC)**: Enforces clear permission boundaries separating customer application flows from credit-officer review and auditing workflows.
* **JWT Authentication**: Secure token-based access across all submission, approval history, and administrative analytics endpoints.
* **Embedded SQLite Database**: Lightweight database setup with indexed schemas for rapid local development and audit logging.

---

## 🏗️ System Architecture & Workflow

```text
                               ┌───────────────────────────────────┐
                               │       Raw Applicant Data          │
                               └─────────────────┬─────────────────┘
                                                 │
                                                 ▼
                               ┌───────────────────────────────────┐
                               │    Feature Engineering Layer      │
                               │   (DTI, LTI, EMI, Disposable)    │
                               └─────────────────┬─────────────────┘
                                                 │
                        ┌────────────────────────┴────────────────────────┐
                        │                                                 │
                        ▼                                                 ▼
    ┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
    │     Rule-Based Compliance Engine     │          │     ML Risk Probability Model        │
    │   (Policy Limits & Regulatory)       │          │   (scikit-learn Classifier)          │
    └───────────────────┬──────────────────┘          └───────────────────┬──────────────────┘
                        │                                                 │
                        └────────────────────────┬────────────────────────┘
                                                 │
                                                 ▼
                               ┌───────────────────────────────────┐
                               │      Weighted Hybrid Scorer       │
                               └─────────────────┬─────────────────┘
                                                 │
                                                 ▼
                       ┌─────────────────────────────────────────────────┐
                       │ Final Decision: APPROVED / REVIEW / REJECTED   │
                       └─────────────────────────────────────────────────┘

```

---

## 🛠️ Tech Stack

* **Core Framework**: Python 3.10+
* **API Engine**: FastAPI, Pydantic, Uvicorn
* **Machine Learning & Analytics**: scikit-learn, NumPy, Pandas
* **Database**: SQLite
* **Security & Authentication**: PyJWT, Passlib (Bcrypt hashing)

---

## 📁 Project Structure

```text
creditRisk/
├── data/
│   ├── raw_applicants.csv      # Sample training dataset
│   └── database.sqlite         # Local SQLite storage (auto-generated)
├── models/
│   ├── train_model.py          # Model training pipeline script
│   └── risk_model.pkl          # Serialized scikit-learn model
├── src/
│   ├── auth/                   # JWT generation, hashing, and RBAC middleware
│   │   ├── dependencies.py
│   │   └── security.py
│   ├── engine/                 # Core scoring logic
│   │   ├── feature_engineering.py
│   │   ├── hybrid_scorer.py
│   │   └── rules.py
│   ├── database/               # DB connection, models, and schemas
│   │   ├── models.py
│   │   └── database.py
│   └── routes/                 # FastAPI endpoints
│       ├── applications.py
│       ├── auth.py
│       └── officer_review.py
├── config.py                   # Central settings and parameters
├── main.py                     # FastAPI application entrypoint
├── requirements.txt            # Project dependencies
└── README.md

```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* `pip` package manager

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Aayupro/creditRisk.git
cd creditRisk

```


2. **Create and activate a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies**:
```bash
pip install -r requirements.txt

```



### Environment Setup

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_super_secret_jwt_key_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./data/database.sqlite

```

---

## 🛠️ Usage

### 1. Database Migration & Setup

Initialize the SQLite database schema:

```bash
python -m src.database.init_db

```

### 2. Model Training

Train the machine learning risk prediction model on applicant data:

```bash
python models/train_model.py

```

### 3. Running the FastAPI Server

Start the application with Uvicorn:

```bash
uvicorn main:app --reload

```

The interactive API documentation (Swagger UI) will be available at:
`[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

---

## 🔌 API Reference

### Authentication

* `POST /api/v1/auth/register` - Create new customer or officer accounts
* `POST /api/v1/auth/login` - Authenticate user and receive JWT bearer token

### Applicant Flow (`Role: Customer`)

* `POST /api/v1/applications/submit` - Submit financial details for automated underwriting
* `GET /api/v1/applications/history` - View previous loan applications and status updates

### Credit Officer Flow (`Role: Credit_Officer`)

* `GET /api/v1/officer/pending` - List applications flagged for `MANUAL_REVIEW`
* `POST /api/v1/officer/review/{app_id}` - Override or finalize credit decisions
* `GET /api/v1/officer/analytics` - System-wide approval rates, risk distribution, and portfolio metrics

---

## 📐 Hybrid Scoring Methodology

The decision engine calculates a unified score between **0** and **100**:

$$\text{Final Score} = (\text{Compliance Score} \times W_{\text{rules}}) + ((1 - \text{Default Probability}) \times 100 \times W_{\text{ML}})$$

### Decision Thresholds

* **Score ≥ 75**: `APPROVED`
* **50 ≤ Score < 75**: `MANUAL_REVIEW` (Sent to Credit Officer queue)
* **Score < 50**: `REJECTED`

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
