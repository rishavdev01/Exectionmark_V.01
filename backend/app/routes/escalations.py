"""
Escalations route — CRUD (maps to PMRiskEscalation, RiskEscalations)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.database import escalations_collection

router = APIRouter()


class EscalationCreate(BaseModel):
    time: str
    event: str
    who: str
    status: str = "Open"
    severity: str = "Medium"


@router.get("")
async def get_escalations(
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
):
    query = {}
    if status:
        query["status"] = status
    if severity:
        query["severity"] = severity
    escalations = []
    async for e in escalations_collection.find(query, {"_id": 0}):
        escalations.append(e)
    return escalations


@router.post("")
async def create_escalation(body: EscalationCreate):
    await escalations_collection.insert_one(body.model_dump())
    return {"message": "Escalation created"}


@router.put("/{index}")
async def update_escalation(index: int, body: dict):
    all_esc = []
    async for e in escalations_collection.find({}, {"_id": 1}):
        all_esc.append(e)
    if index >= len(all_esc):
        raise HTTPException(status_code=404, detail="Escalation not found")
    result = await escalations_collection.update_one(
        {"_id": all_esc[index]["_id"]}, {"$set": body}
    )
    return {"message": "Escalation updated"}
