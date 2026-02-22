"""
Pipelines route — CRUD (maps to DevOpsDashboard, DevOpsPipelines)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import pipelines_collection

router = APIRouter()


class PipelineCreate(BaseModel):
    id: int
    name: str
    status: str = "Passed"
    branch: str = "main"
    duration: str = ""
    triggered: str = ""


@router.get("")
async def get_pipelines():
    pipelines = []
    async for p in pipelines_collection.find({}, {"_id": 0}):
        pipelines.append(p)
    return pipelines


@router.post("")
async def create_pipeline(body: PipelineCreate):
    await pipelines_collection.insert_one(body.model_dump())
    return {"message": "Pipeline created"}


@router.put("/{pipeline_id}")
async def update_pipeline(pipeline_id: int, body: dict):
    result = await pipelines_collection.update_one({"id": pipeline_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"message": "Pipeline updated"}
