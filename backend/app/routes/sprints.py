"""
Sprints route — CRUD + stories for a sprint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import sprints_collection, stories_collection

router = APIRouter()


class SprintCreate(BaseModel):
    id: str
    name: str
    status: str = "Active"
    startDate: str = ""
    endDate: str = ""
    velocity: int = 0
    storyPoints: int = 0
    completion: int = 0
    health: str = "Healthy"
    daysLeft: int = 0
    totalStories: int = 0
    completedStories: int = 0


@router.get("")
async def get_sprints():
    sprints = []
    async for s in sprints_collection.find({}, {"_id": 0}):
        sprints.append(s)
    return sprints


@router.get("/{sprint_id}")
async def get_sprint(sprint_id: str):
    sprint = await sprints_collection.find_one({"id": sprint_id}, {"_id": 0})
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint


@router.get("/{sprint_id}/stories")
async def get_sprint_stories(sprint_id: str):
    stories = []
    async for s in stories_collection.find({"sprint_id": sprint_id}, {"_id": 0}):
        stories.append(s)
    return stories


@router.post("")
async def create_sprint(body: SprintCreate):
    await sprints_collection.insert_one(body.model_dump())
    return {"message": "Sprint created"}


@router.put("/{sprint_id}")
async def update_sprint(sprint_id: str, body: dict):
    result = await sprints_collection.update_one({"id": sprint_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return {"message": "Sprint updated"}
