"""
Deployments route — CRUD (maps to DevOpsDashboard, DevOpsDeployments)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import deployments_collection

router = APIRouter()


class DeploymentCreate(BaseModel):
    id: int
    service: str
    env: str = "Production"
    version: str = ""
    time: str = ""
    status: str = "Success"


@router.get("")
async def get_deployments():
    deployments = []
    async for d in deployments_collection.find({}, {"_id": 0}):
        deployments.append(d)
    return deployments


@router.post("")
async def create_deployment(body: DeploymentCreate):
    await deployments_collection.insert_one(body.model_dump())
    return {"message": "Deployment created"}


@router.put("/{deployment_id}")
async def update_deployment(deployment_id: int, body: dict):
    result = await deployments_collection.update_one({"id": deployment_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return {"message": "Deployment updated"}
