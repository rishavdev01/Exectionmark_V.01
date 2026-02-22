"""
Projects route — CRUD (maps to CEOProjects.jsx)
"""

from fastapi import APIRouter, HTTPException

from app.database import projects_collection

router = APIRouter()




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
async def create_project(body: dict):
    body.pop("_id", None)
    await projects_collection.insert_one(body)
    return {"message": "Project created"}


@router.put("/{project_id}")
async def update_project(project_id: str, body: dict):
    result = await projects_collection.update_one({"id": project_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project updated"}
