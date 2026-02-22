"""
Company model — seeded in backend only, not exposed in frontend registration.
"""

from pydantic import BaseModel
from typing import Optional


class Company(BaseModel):
    company_id: str          # e.g. 'COMP-001'
    name: str                # e.g. 'Exactiomark Technologies'
    org_password: str        # hashed organisation-wide gate password
    admin: str               # admin username / email
    admin_password: str      # hashed admin password


class CompanyOut(BaseModel):
    """Safe response model — excludes passwords."""
    company_id: str
    name: str
    admin: str
