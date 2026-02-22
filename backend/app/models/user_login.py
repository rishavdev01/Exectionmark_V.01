from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    """
    User login credentials model.
    employee_id: unique employee identifier (e.g. 'EMP-001')
    org_password: hashed organisation-wide gate password
    user_password: hashed personal password
    """
    id: str
    employee_id: str        # e.g. 'EMP-001'
    name: str
    email: str
    role: str               # CEO | HR | PM | LEAD | DEVELOPER | DEVOPS | QA
    org_password: str       # bcrypt hashed — org-wide gate password
    user_password: str      # bcrypt hashed — personal password
    created_at: str
    is_active: bool = True
