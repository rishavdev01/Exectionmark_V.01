"""
Reports route — CRUD (maps to ReportsPage, CEOReports, HRReports, etc.)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.database import reports_collection

router = APIRouter()


class ReportCreate(BaseModel):
    id: int
    title: str
    type: str = "Performance"
    date: str = ""
    role: str = ""
    desc: str = ""
    lastGenerated: str = ""


@router.get("")
async def get_reports(role: Optional[str] = Query(None), type: Optional[str] = Query(None)):
    query = {}
    if role:
        query["role"] = role
    if type:
        query["type"] = type
    reports = []
    async for r in reports_collection.find(query, {"_id": 0}):
        reports.append(r)
    return reports


@router.post("")
async def create_report(body: ReportCreate):
    await reports_collection.insert_one(body.model_dump())
    return {"message": "Report created"}
