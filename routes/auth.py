from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from database.db import get_db
from utils.auth_utils import hash_password, verify_password, create_access_token
import sqlite3

router = APIRouter()

# Separate schemas for registration vs login to prevent validation issues
class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: UserRegisterSchema):
    conn = next(get_db())
    cursor = conn.cursor()
    try:
        role = "officer" if "officer" in data.email else "customer"
        cursor.execute("INSERT INTO users (email, password, role, full_name) VALUES (?, ?, ?, ?)",
                       (data.email, hash_password(data.password), role, data.full_name))
        conn.commit()
        return {"msg": "Success"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User exists")

@router.post("/login")
def login(data: UserLoginSchema):
    conn = next(get_db())
    cursor = conn.cursor()
    cursor.execute("SELECT id, password, role, full_name FROM users WHERE email = ?", (data.email,))
    user = cursor.fetchone()
    if not user or not verify_password(data.password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid Credentials")
    
    token = create_access_token({"sub": user['id'], "role": user['role'], "name": user['full_name']})
    return {"access_token": token, "role": user['role'], "name": user['full_name']}