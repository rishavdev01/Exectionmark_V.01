"""
Stories route — CRUD + filters (maps to BacklogStories, PMTasks stories)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.database import stories_collection

router = APIRouter()


class StoryCreate(BaseModel):
    id: str
    title: str
    assignee: str = ""
    type: str = "Dev"
    alignment: int = 0
    risk: str = "Low"
    approval: str = "Not Started"
    delay: int = 0
    est: str = ""
    actual: str = "—"
    status: str = "To Do"
    sprint_id: str = ""
    priority: str = "Medium"
    storyPoints: int = 0
    description: str = ""
    desc: str = ""
    module: str = ""


@router.get("")
async def get_stories(
    status: Optional[str] = Query(None),
    risk: Optional[str] = Query(None),
    assignee: Optional[str] = Query(None),
    sprint_id: Optional[str] = Query(None),
):
    query = {}
    if status:
        query["status"] = status
    if risk:
        query["risk"] = risk
    if assignee:
        query["assignee"] = assignee
    if sprint_id:
        query["sprint_id"] = sprint_id
    stories = []
    async for s in stories_collection.find(query, {"_id": 0}):
        stories.append(s)
    return stories


@router.get("/{story_id}")
async def get_story(story_id: str):
    story = await stories_collection.find_one({"id": story_id}, {"_id": 0})
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.post("")
async def create_story(body: StoryCreate):
    await stories_collection.insert_one(body.model_dump())
    return {"message": "Story created"}


@router.put("/{story_id}")
async def update_story(story_id: str, body: dict):
    result = await stories_collection.update_one({"id": story_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"message": "Story updated"}


@router.delete("/{story_id}")
async def delete_story(story_id: str):
    result = await stories_collection.delete_one({"id": story_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"message": "Story deleted"}
