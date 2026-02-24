"""
Auth route — POST /api/auth/login

Login requires: employee_id + organisation_password + employee_password
All passwords are verified against bcrypt hashes stored in user_logins.
"""

import bcrypt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import db

router = APIRouter()


# ── Request / Response schemas ────────────────────────────────────────────────

class LoginRequest(BaseModel):
    employee_id:           str
    organisation_password: str   # plain-text — verified against stored hash
    employee_password:     str   # plain-text — verified against stored hash


class LoginResponse(BaseModel):
    employee_id: str
    name:        str
    email:       str
    role:        str
    dept:        str
    avatar:      Optional[str] = None
    is_active:   bool


# ── Helper ────────────────────────────────────────────────────────────────────

def _verify(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest):
    # Look up employee by employee_id in user_logins
    user = await db["user_logins"].find_one({"employee_id": body.employee_id})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid employee ID or password")

    # Verify organisation password
    if not _verify(body.organisation_password, user.get("organisation_password", "")):
        raise HTTPException(status_code=401, detail="Invalid company password")

    # Verify employee password
    if not _verify(body.employee_password, user.get("employee_password", "")):
        raise HTTPException(status_code=401, detail="Invalid employee password")

    # Check active status
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account is inactive")

    return LoginResponse(
        employee_id = user["employee_id"],
        name        = user["name"],
        email       = user["email"],
        role        = user["role"],
        dept        = user["dept"],
        avatar      = user.get("avatar"),
        is_active   = user["is_active"],
    )
