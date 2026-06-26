import sqlite3

DB_NAME = "credit_risk_engine.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Users System
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    
    # Applications Core Schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT, age INTEGER, gender TEXT, occupation TEXT,
            annual_income REAL, monthly_income REAL, existing_loans INTEGER,
            existing_emis REAL, loan_amount REAL, loan_purpose TEXT,
            loan_tenure INTEGER, employment_type TEXT, years_of_employment REAL,
            credit_score INTEGER, dependents INTEGER, assets REAL, liabilities REAL,
            status TEXT DEFAULT 'Pending',
            rule_score REAL, ml_prob REAL, risk_category TEXT, decision TEXT,
            explanation TEXT, created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Seed default user profiles safely if missing
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        cursor.execute("INSERT INTO users (email, password, role, full_name) VALUES (?, ?, ?, ?)",
                       ("officer@bank.com", pwd_context.hash("officer123"), "officer", "Agent Smith"))
        cursor.execute("INSERT INTO users (email, password, role, full_name) VALUES (?, ?, ?, ?)",
                       ("customer@client.com", pwd_context.hash("customer123"), "customer", "John Doe"))
    
    conn.commit()
    conn.close()