from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.database import (
    behaviour_history_collection, behaviour_ratings_collection,
    candidates_collection, dept_performance_collection,
    sprint_velocity_collection, performers_collection,
    audit_log_collection, hr_reports_collection, company_settings_collection,
)
from app.models.hr_models import (
    BehaviourHistory, BehaviourRating, Candidate,
    DeptPerformance, SprintVelocity, Performer,
    AuditLog, HRReport, CompanySettings,
)

router = APIRouter()


# ── Behaviour History ──
@router.get("/behaviour/history", response_model=list[BehaviourHistory])
async def get_behaviour_history(member: Optional[str] = Query(None)):
    query = {}
    if member: query["member"] = member
    return [doc async for doc in behaviour_history_collection.find(query, {"_id": 0})]


# ── Behaviour Ratings ──
@router.get("/behaviour/ratings", response_model=list[BehaviourRating])
async def get_behaviour_ratings(member: Optional[str] = Query(None), sprint: Optional[str] = Query(None)):
    query = {}
    if member: query["member"] = member
    if sprint: query["sprint"] = sprint
    return [doc async for doc in behaviour_ratings_collection.find(query, {"_id": 0})]


@router.post("/behaviour/ratings", response_model=dict)
async def create_behaviour_rating(body: BehaviourRating):
    await behaviour_ratings_collection.insert_one(body.model_dump())
    return {"message": "Rating submitted"}


# ── Candidates ──
@router.get("/candidates", response_model=list[Candidate])
async def get_candidates(status: Optional[str] = Query(None), role: Optional[str] = Query(None)):
    query = {}
    if status: query["status"] = status
    if role: query["role"] = role
    return [doc async for doc in candidates_collection.find(query, {"_id": 0})]


@router.post("/candidates", response_model=dict)
async def create_candidate(body: Candidate):
    await candidates_collection.insert_one(body.model_dump())
    return {"message": "Candidate added"}


@router.put("/candidates/{cand_id}", response_model=dict)
async def update_candidate(cand_id: str, body: dict):
    body.pop("_id", None)
    result = await candidates_collection.update_one({"id": int(cand_id)}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Candidate not found")
    return {"message": "Updated"}


@router.delete("/candidates/{cand_id}", response_model=dict)
async def delete_candidate(cand_id: str):
    await candidates_collection.delete_one({"id": int(cand_id)})
    return {"message": "Removed"}


# ── Department Performance ──
@router.get("/performance/dept", response_model=list[DeptPerformance])
async def get_dept_performance():
    return [doc async for doc in dept_performance_collection.find({}, {"_id": 0})]


# ── Sprint Velocity ──
@router.get("/performance/velocity", response_model=list[SprintVelocity])
async def get_sprint_velocity():
    return [doc async for doc in sprint_velocity_collection.find({}, {"_id": 0})]


# ── Performers ──
@router.get("/performance/performers", response_model=list[Performer])
async def get_performers(type: Optional[str] = Query(None)):
    query = {}
    if type: query["type"] = type
    return [doc async for doc in performers_collection.find(query, {"_id": 0})]


# ── Audit Log ──
@router.get("/audit-log", response_model=list[AuditLog])
async def get_audit_log():
    return [doc async for doc in audit_log_collection.find({}, {"_id": 0}).sort("time", -1)]


@router.post("/audit-log", response_model=dict)
async def create_audit_log(body: AuditLog):
    await audit_log_collection.insert_one(body.model_dump())
    return {"message": "Audit log entry created"}


# ── HR Reports ──
@router.get("/reports", response_model=list[HRReport])
async def get_hr_reports():
    return [doc async for doc in hr_reports_collection.find({}, {"_id": 0})]


# ── Company Settings ──
@router.get("/company-settings")
async def get_company_settings():
    doc = await company_settings_collection.find_one({}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "Company settings not configured")
    return doc


@router.put("/company-settings", response_model=dict)
async def update_company_settings(body: dict):
    body.pop("_id", None)
    await company_settings_collection.update_one({}, {"$set": body}, upsert=True)
    return {"message": "Company settings updated"}
