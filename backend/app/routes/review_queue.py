"""
Review Queue route — CRUD + actions (maps to PMReviewQueue, SMReviewQueue)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import review_queue_collection

router = APIRouter()


class ReviewItemCreate(BaseModel):
    id: str
    task: str
    submittedBy: str = ""
    alignment: int = 0
    leadApproval: str = "Pending"
    delay: int = 0
    risk: str = "Low"
    aiComment: str = ""


class ReviewAction(BaseModel):
    action: str  # approve | reject | revision
    comment: str = ""


@router.get("")
async def get_review_queue():
    items = []
    async for r in review_queue_collection.find({}, {"_id": 0}):
        items.append(r)
    return items


@router.post("")
async def create_review_item(body: ReviewItemCreate):
    await review_queue_collection.insert_one(body.model_dump())
    return {"message": "Review item created"}


@router.put("/{item_id}/action")
async def review_action(item_id: str, body: ReviewAction):
    status_map = {"approve": "Approved", "reject": "Rejected", "revision": "Revision"}
    new_status = status_map.get(body.action, "Pending")
    result = await review_queue_collection.update_one(
        {"id": item_id},
        {"$set": {"leadApproval": new_status}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review item not found")
    return {"message": f"Item {body.action}d"}
