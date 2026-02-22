"""
Candidates route — CRUD (maps to CEOHiring.jsx, HRInvitations.jsx)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.database import candidates_collection

router = APIRouter()


class CandidateCreate(BaseModel):
    id: int
    name: str
    email: str = ""
    role: str = ""
    status: str = "Pending"
    department: str = ""
    project: str = ""
    date: str = ""
    experience: str = ""
    match: int = 0
    source: str = ""


@router.get("")
async def get_candidates(
    status: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
):
    query = {}
    if status:
        query["status"] = status
    if role:
        query["role"] = role
    candidates = []
    async for c in candidates_collection.find(query, {"_id": 0}):
        candidates.append(c)
    return candidates


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: int):
    c = await candidates_collection.find_one({"id": candidate_id}, {"_id": 0})
    if not c:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return c


@router.post("")
async def create_candidate(body: CandidateCreate):
    await candidates_collection.insert_one(body.model_dump())
    return {"message": "Candidate created"}


@router.put("/{candidate_id}")
async def update_candidate(candidate_id: int, body: dict):
    result = await candidates_collection.update_one({"id": candidate_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate updated"}


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: int):
    result = await candidates_collection.delete_one({"id": candidate_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted"}
