"""
System Health route — CRUD (maps to DevOpsDashboard, DevOpsSystemHealth)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import system_health_collection

router = APIRouter()


class HealthCreate(BaseModel):
    service: str
    cpu: float = 0
    memory: float = 0
    uptime: float = 99.9


@router.get("")
async def get_health():
    health = []
    async for h in system_health_collection.find({}, {"_id": 0}):
        health.append(h)
    return health


@router.post("")
async def create_health(body: HealthCreate):
    await system_health_collection.insert_one(body.model_dump())
    return {"message": "Health record created"}


@router.put("/{service_name}")
async def update_health(service_name: str, body: dict):
    result = await system_health_collection.update_one({"service": service_name}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Health updated"}
