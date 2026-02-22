from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.database import (
    execution_weeks_collection, sprint_status_slices_collection,
    ceo_escalations_collection, health_factors_collection,
    story_risks_collection, dev_risk_contributions_collection,
    active_risks_collection, escalation_events_collection,
    risk_patterns_collection, performance_members_collection,
    ceo_improvements_collection, ceo_behaviour_feedback_collection,
)
from app.models.ceo_models import SaveBehaviourFeedback, CEOBehaviourFeedback

router = APIRouter()


@router.get("/execution-data")
async def get_execution_data():
    return [doc async for doc in execution_weeks_collection.find({}, {"_id": 0})]


@router.get("/sprint-status")
async def get_sprint_status():
    return [doc async for doc in sprint_status_slices_collection.find({}, {"_id": 0})]


@router.get("/escalations")
async def get_ceo_escalations(status: Optional[str] = Query(None)):
    query = {}
    if status:
        query["status"] = status
    return [doc async for doc in ceo_escalations_collection.find(query, {"_id": 0})]


@router.get("/health-factors")
async def get_health_factors():
    return [doc async for doc in health_factors_collection.find({}, {"_id": 0})]


@router.get("/story-risks")
async def get_story_risks():
    return [doc async for doc in story_risks_collection.find({}, {"_id": 0}).sort("risk", -1)]


@router.get("/dev-risk")
async def get_dev_risk():
    return [doc async for doc in dev_risk_contributions_collection.find({}, {"_id": 0})]


@router.get("/active-risks")
async def get_active_risks(riskLevel: Optional[str] = Query(None)):
    query = {}
    if riskLevel:
        query["riskLevel"] = riskLevel
    return [doc async for doc in active_risks_collection.find(query, {"_id": 0})]


@router.get("/escalation-timeline")
async def get_escalation_timeline():
    return [doc async for doc in escalation_events_collection.find({}, {"_id": 0})]


@router.get("/risk-patterns")
async def get_risk_patterns():
    return [doc async for doc in risk_patterns_collection.find({}, {"_id": 0})]


@router.get("/performance-members")
async def get_performance_members(promotion: Optional[bool] = Query(None)):
    query = {}
    if promotion is not None:
        query["promotion"] = promotion
    return [doc async for doc in performance_members_collection.find(query, {"_id": 0})]


@router.get("/improvements")
async def get_ceo_improvements():
    return [doc async for doc in ceo_improvements_collection.find({}, {"_id": 0})]


@router.get("/behaviour-feedback")
async def get_ceo_behaviour_feedback():
    return [doc async for doc in ceo_behaviour_feedback_collection.find({}, {"_id": 0})]


@router.post("/behaviour-feedback", response_model=dict)
async def save_behaviour_feedback(body: SaveBehaviourFeedback):
    """Save behaviour scores from Performance Insights. Upserts ceo_behaviour_feedback and updates performance_members."""
    # Clamp criteria to 1-10
    communication = max(1, min(10, body.communication))
    ownership = max(1, min(10, body.ownership))
    teamwork = max(1, min(10, body.teamwork))
    adaptability = max(1, min(10, body.adaptability))
    behaviour_avg = round((communication + ownership + teamwork + adaptability) / 4.0, 1)

    # Upsert feedback doc
    existing_feedback = await ceo_behaviour_feedback_collection.find_one({"name": body.name}, {"_id": 0, "id": 1})
    feedback_id = existing_feedback["id"] if existing_feedback else f"cbf-{body.name.lower().replace(' ', '-')}"
    
    feedback_doc = CEOBehaviourFeedback(
        id=feedback_id,
        name=body.name,
        communication=communication,
        ownership=ownership,
        teamwork=teamwork,
        adaptability=adaptability,
        notes=body.notes or "",
    )
    await ceo_behaviour_feedback_collection.update_one(
        {"name": body.name},
        {"$set": feedback_doc.model_dump()},
        upsert=True,
    )

    # Fetch performance member to recalculate overall
    member = await performance_members_collection.find_one({"name": body.name})
    if not member:
        raise HTTPException(404, f"Performance member not found: {body.name}")

    # New Weights: Sprint Contrib 40%, Alignment 30%, Delivery (onTime) 20%, Behaviour 10%
    # Note: sprintContrib defaults to 85 if missing
    sprint_contrib = member.get("sprintContrib", 85)
    alignment = member.get("alignment", 80)
    on_time = member.get("onTime", 85)
    
    overall = (
        (sprint_contrib * 0.4) +
        (alignment * 0.3) +
        (on_time * 0.2) +
        (behaviour_avg * 10 * 0.1)
    )
    overall = round(overall, 1)

    await performance_members_collection.update_one(
        {"name": body.name},
        {"$set": {
            "behaviour": behaviour_avg,
            "overall": overall
        }},
    )

    return {"ok": True, "behaviour": behaviour_avg, "overall": overall}
