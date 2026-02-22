"""
Projects route — CRUD (maps to CEOProjects.jsx)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.database import projects_collection

router = APIRouter()


class ProjectCreate(BaseModel):
    id: str
    name: str
    budget: str = ""
    burnRate: str = ""
    status: str = "Active"
    lead: str = ""
    team: List[str] = []
    timeline: str = ""
    completion: int = 0
    health: str = "Healthy"


@router.get("")
async def get_projects():
    projects = []
    async for p in projects_collection.find({}, {"_id": 0}):
        projects.append(p)
    return projects


@router.get("/{project_id}")
async def get_project(project_id: str):
    project = await projects_collection.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("")
async def create_project(body: ProjectCreate):
    await projects_collection.insert_one(body.model_dump())
    return {"message": "Project created"}


@router.put("/{project_id}")
async def update_project(project_id: str, body: dict):
    result = await projects_collection.update_one({"id": project_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project updated"}
