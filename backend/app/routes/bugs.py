"""
Bugs route — CRUD (maps to QADashboard, QABugReports)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.database import bugs_collection

router = APIRouter()


class BugCreate(BaseModel):
    id: int
    name: str
    status: str = "Open"
    priority: str = "Medium"
    assignee: str = ""
    description: str = ""
    color: str = "#ef4444"


@router.get("")
async def get_bugs(status: Optional[str] = Query(None)):
    query = {}
    if status:
        query["status"] = status
    bugs = []
    async for b in bugs_collection.find(query, {"_id": 0}):
        bugs.append(b)
    return bugs


@router.post("")
async def create_bug(body: BugCreate):
    await bugs_collection.insert_one(body.model_dump())
    return {"message": "Bug created"}


@router.put("/{bug_id}")
async def update_bug(bug_id: int, body: dict):
    result = await bugs_collection.update_one({"id": bug_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Bug not found")
    return {"message": "Bug updated"}
