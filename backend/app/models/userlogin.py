"""
userlogin.py — Pydantic models for employee-as-user authentication.

Each employee IS a user. A single document in `user_logins` contains:
  ── Auth fields (required) ──────────────────────────────────────────
  - employee_id           : unique identifier (e.g. EMP-CEO-001)
  - name                  : login handle / display name
  - email                 : work email
  - phone                 : contact number
  - organisation_password : bcrypt hash — set by the organisation / HR
  - employee_password     : bcrypt hash — set by the employee
  - role                  : CEO / HR / PM / LEAD / DEVELOPER / DEVOPS / QA
  - is_active             : account enabled flag

  ── Profile / performance fields (optional) ─────────────────────────
  - dept, avatar, projects, status
  - perfScore, behaviour, risk, sprintContrib
  - alignment, onTime, rejection
  - alignmentHistory, sprintTrend, behaviourScores
  - managerComment, riskData, promotion
  - sprintTasks, workload

Login requires: employee_id + organisation_password + employee_password
"""

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr


# ── Helper ────────────────────────────────────────────────────────────────────

def generate_employee_id() -> str:
    """Generate a unique employee ID prefixed with 'EMP-' followed by a UUID4."""
    return f"EMP-{uuid.uuid4()}"


# ── DB document ───────────────────────────────────────────────────────────────

class EmployeeUserDB(BaseModel):
    """
    Full employee-user document stored in the `user_logins` collection.
    Auth fields are required; profile fields are optional so the document
    can be created at registration and enriched later.
    """
    # ── Auth (required) ──
    employee_id:           str      = Field(default_factory=generate_employee_id)
    name:                  str      = Field(..., description="Login handle / display name.")
    email:                 EmailStr = Field(..., description="Unique work email.")
    phone:                 str      = Field(..., description="Contact phone number.")
    organisation_password: str      = Field(..., description="Bcrypt hash — set by HR.")
    employee_password:     str      = Field(..., description="Bcrypt hash — set by employee.")
    role:                  str      = Field(..., description="CEO/HR/PM/LEAD/DEVELOPER/DEVOPS/QA")
    is_active:             bool     = Field(default=True)

    # ── Profile (optional — populated by HR/system) ──
    dept:             str                      = Field(..., description="Department name, e.g. Engineering, HR.")
    avatar:           Optional[str]            = None
    projects:         Optional[List[str]]      = None
    status:           Optional[str]            = None   # Active / Probation / On Leave

    # ── Performance metrics ──
    perfScore:        Optional[float]          = None
    behaviour:        Optional[float]          = None
    risk:             Optional[str]            = None   # Low / Medium / High
    sprintContrib:    Optional[str]            = None   # e.g. "24 SP"
    alignment:        Optional[int]            = None
    onTime:           Optional[int]            = None
    rejection:        Optional[int]            = None

    # ── History / trends ──
    alignmentHistory: Optional[List[Dict[str, Any]]] = None
    sprintTrend:      Optional[List[Dict[str, Any]]] = None
    behaviourScores:  Optional[Dict[str, Any]]       = None

    # ── Review / promotion ──
    managerComment:   Optional[str]            = None
    riskData:         Optional[Dict[str, Any]] = None
    promotion:        Optional[Dict[str, Any]] = None

    # ── Workload ──
    sprintTasks:      Optional[int]            = None
    workload:         Optional[int]            = None


# ── Request: create a new employee user ──────────────────────────────────────

class EmployeeUserCreate(BaseModel):
    """Payload used when HR creates a new employee user account (plain-text passwords)."""
    name:                  str
    email:                 EmailStr
    phone:                 str
    organisation_password: str    # hashed before persisting
    employee_password:     str    # hashed before persisting
    role:                  str
    is_active:             bool = True


# ── Request: login ────────────────────────────────────────────────────────────

class EmployeeUserLogin(BaseModel):
    """
    Login payload.
    The employee must supply their employee_id plus BOTH passwords.
    """
    employee_id:           str
    organisation_password: str    # verified against stored hash
    employee_password:     str    # verified against stored hash


# ── Response (never exposes password hashes) ──────────────────────────────────

class EmployeeUserOut(BaseModel):
    """Safe employee-user representation returned to the client."""
    employee_id: str
    name:        str
    email:       EmailStr
    phone:       str
    role:        str
    dept:        Optional[str] = None
    avatar:      Optional[str] = None
    status:      Optional[str] = None
    is_active:   bool
