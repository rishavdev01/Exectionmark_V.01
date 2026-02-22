"""
Alerts route — CRUD (maps to DevOpsDashboard, DevOpsLogsAlerts)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.database import alerts_collection

router = APIRouter()


class AlertCreate(BaseModel):
    id: int
    msg: str
    level: str = "info"
    time: str = ""


@router.get("")
async def get_alerts(level: Optional[str] = Query(None)):
    query = {}
    if level:
        query["level"] = level
    alerts = []
    async for a in alerts_collection.find(query, {"_id": 0}):
        alerts.append(a)
    return alerts


@router.post("")
async def create_alert(body: AlertCreate):
    await alerts_collection.insert_one(body.model_dump())
    return {"message": "Alert created"}


@router.delete("/{alert_id}")
async def delete_alert(alert_id: int):
    result = await alerts_collection.delete_one({"id": alert_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted"}
