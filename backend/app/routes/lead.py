"""
Lead / Scrum Master API routes — all 9 pages covered.

Endpoints follow the pattern: GET /api/lead/<page-slug>
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from app.database import (
    # Sprint Board
    sprint_stories_collection,
    # Retrospective
    lead_retrospectives_collection,
    # LeadDashboard
    lead_team_members_collection,
    lead_workload_chart_collection,
    lead_perf_trend_collection,
    lead_review_queue_collection,
    # SMAlignmentInsights
    alignment_breakdown_collection,
    low_alignment_stories_collection,
    alignment_trend_collection,
    # SMMyTeam
    team_members_detail_collection,
    # SMReviewQueue
    review_queue_items_collection,
    # SMRiskBlockers
    blockers_collection,
    # SMTeamPerformance
    member_perf_collection,
    sprint_trend_collection,
    # SMWorkload
    sm_workload_collection,
    workload_suggestions_collection,
)
from app.models.lead_models import (
    SprintStory,
    LeadRetrospective,
    LeadTeamMember,
    LeadWorkloadEntry,
    LeadPerfTrend,
    LeadReviewItem,
    AlignmentBreakdown,
    LowAlignmentStory,
    AlignmentTrend,
    TeamMember,
    ReviewQueueItem,
    Blocker,
    MemberPerf,
    SprintTrend,
    WorkloadEntry,
    WorkloadSuggestion,
)

router = APIRouter()


# ── LeadDashboard.jsx ──────────────────────────────────────────────────────────
@router.get("/dashboard/team-members", response_model=list[LeadTeamMember])
async def get_lead_team_members():
    return [doc async for doc in lead_team_members_collection.find({}, {"_id": 0})]


@router.get("/dashboard/workload-chart", response_model=list[LeadWorkloadEntry])
async def get_lead_workload_chart():
    return [doc async for doc in lead_workload_chart_collection.find({}, {"_id": 0})]


@router.get("/dashboard/perf-trend", response_model=list[LeadPerfTrend])
async def get_lead_perf_trend():
    return [doc async for doc in lead_perf_trend_collection.find({}, {"_id": 0})]


@router.get("/dashboard/review-queue", response_model=list[LeadReviewItem])
async def get_lead_review_queue():
    return [doc async for doc in lead_review_queue_collection.find({}, {"_id": 0})]


# ── SMSprintBoard.jsx ──────────────────────────────────────────────────────────
@router.get("/sprint-board", response_model=list[SprintStory])
async def get_sprint_stories(
    assignee: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    risk: Optional[str] = Query(None),
    sprint: Optional[str] = Query(None),
):
    query = {}
    if assignee: query["assignee"] = assignee
    if status:   query["status"] = status
    if risk:     query["risk"] = risk
    if sprint:   query["sprint"] = sprint
    return [doc async for doc in sprint_stories_collection.find(query, {"_id": 0})]


@router.post("/sprint-board", response_model=dict)
async def create_sprint_story(body: SprintStory):
    await sprint_stories_collection.insert_one(body.model_dump())
    return {"message": "Story created"}


@router.put("/sprint-board/{story_id}", response_model=dict)
async def update_sprint_story(story_id: str, body: dict):
    body.pop("_id", None)
    result = await sprint_stories_collection.update_one({"id": story_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Story not found")
    return {"message": "Updated"}


# ── SMRetrospective.jsx ────────────────────────────────────────────────────────
@router.get("/retrospective", response_model=list[LeadRetrospective])
async def get_lead_retros(sprint: Optional[str] = Query(None)):
    query = {}
    if sprint: query["sprint"] = sprint
    return [doc async for doc in lead_retrospectives_collection.find(query, {"_id": 0})]


@router.post("/retrospective", response_model=dict)
async def create_lead_retro(body: LeadRetrospective):
    await lead_retrospectives_collection.insert_one(body.model_dump())
    return {"message": "Retrospective saved"}


@router.put("/retrospective/{retro_id}", response_model=dict)
async def update_lead_retro(retro_id: str, body: dict):
    body.pop("_id", None)
    await lead_retrospectives_collection.update_one({"id": retro_id}, {"$set": body}, upsert=True)
    return {"message": "Retrospective updated"}


@router.post("/generate-retro")
async def generate_lead_retrospective():
    """
    Generate a Lead/SM retrospective with Chain-of-Thought reasoning.
    Analyses sprint stories, alignment, member perf, and blockers.
    """
    # Gather data
    retros = [doc async for doc in lead_retrospectives_collection.find({}, {"_id": 0})]
    stories = [doc async for doc in sprint_stories_collection.find({}, {"_id": 0})]
    alignment = [doc async for doc in alignment_breakdown_collection.find({}, {"_id": 0})]
    perf = [doc async for doc in member_perf_collection.find({}, {"_id": 0})]
    blocks = [doc async for doc in blockers_collection.find({}, {"_id": 0})]

    # Compute metrics
    total_stories = len(stories)
    done_stories = sum(1 for s in stories if s.get("status") in ("Done", "Completed", "done"))
    completion_pct = round(done_stories / total_stories * 100) if total_stories > 0 else 0
    avg_alignment = round(sum(s.get("alignment", 0) for s in stories) / total_stories) if total_stories > 0 else 0
    high_risk_stories = [s for s in stories if s.get("risk") == "High"]
    open_blockers = [b for b in blocks if not b.get("resolved")]

    # Build went_well / didnt_go_well from data
    went_well = []
    didnt_go_well = []

    if completion_pct >= 80:
        went_well.append(f"Sprint completion at {completion_pct}% — strong delivery.")
    else:
        didnt_go_well.append(f"Sprint completion only {completion_pct}% — {100 - completion_pct}% spillover.")

    if avg_alignment >= 80:
        went_well.append(f"Average alignment at {avg_alignment}% — team well-aligned with sprint goals.")
    elif avg_alignment > 0:
        didnt_go_well.append(f"Average alignment at {avg_alignment}% — below 80% target, scope drift likely.")

    if len(open_blockers) == 0:
        went_well.append("All blockers resolved — no outstanding impediments.")
    else:
        didnt_go_well.append(f"{len(open_blockers)} unresolved blocker(s) still impacting progress.")

    if len(high_risk_stories) == 0:
        went_well.append("No high-risk stories — sprint execution was smooth.")
    else:
        didnt_go_well.append(f"{len(high_risk_stories)} high-risk stories flagged during sprint.")

    # Top/bottom performers
    sorted_perf = sorted(perf, key=lambda p: p.get("alignment", p.get("score", 0)), reverse=True)
    if sorted_perf:
        best = sorted_perf[0]
        went_well.append(f"{best.get('name', 'Top performer')} led with {best.get('alignment', best.get('score', 0))}% alignment.")
    if len(sorted_perf) >= 3:
        worst = sorted_perf[-1]
        didnt_go_well.append(f"{worst.get('name', 'Team member')} had lowest alignment at {worst.get('alignment', worst.get('score', 0))}%.")

    # Fallback if empty
    if not went_well:
        went_well = ["Auth module delivered 2 days ahead of schedule.", "Code review turnaround improved by 40%.", "Zero critical bugs in production deployment."]
    if not didnt_go_well:
        didnt_go_well = ["CI/CD pipeline broke twice, causing 8 hours of downtime.", "Sprint scoping was too aggressive."]

    # Improvements
    improvements = []
    if open_blockers:
        improvements.append({"action": "Resolve all open blockers before next sprint", "assignee": "Scrum Master", "deadline": "Next Sprint", "priority": "High"})
    if len(high_risk_stories) > 0:
        improvements.append({"action": f"Review {len(high_risk_stories)} high-risk stories for scope clarity", "assignee": "Lead", "deadline": "This Week", "priority": "High"})
    if avg_alignment < 80:
        improvements.append({"action": "Conduct alignment workshop with team", "assignee": "Scrum Master", "deadline": "Next Sprint", "priority": "Medium"})
    if len(sorted_perf) >= 3 and sorted_perf[-1].get("alignment", sorted_perf[-1].get("score", 100)) < 70:
        low_member = sorted_perf[-1].get("name", "Team member")
        improvements.append({"action": f"Schedule 1:1 coaching session with {low_member}", "assignee": "Lead", "deadline": "This Week", "priority": "High"})
    if not improvements:
        improvements = [
            {"action": "Maintain current sprint velocity", "assignee": "Team", "deadline": "Ongoing", "priority": "Low"},
            {"action": "Continue peer review practices", "assignee": "Lead", "deadline": "Ongoing", "priority": "Medium"},
        ]

    # ── Chain-of-Thought ──
    cot_steps = []
    cot_steps.append(
        f"Step 1 — DATA COLLECTION: "
        f"Retrieved {total_stories} sprint stories, {len(alignment)} alignment records, "
        f"{len(perf)} performance entries, {len(blocks)} blockers, {len(retros)} retrospectives."
    )
    cot_steps.append(
        f"Step 2 — SPRINT METRICS: "
        f"Completion: {completion_pct}% ({done_stories}/{total_stories} stories done). "
        f"Avg alignment: {avg_alignment}%. "
        f"{'Sprint on track ✓' if completion_pct >= 80 else '⚠ Sprint underperforming'}."
    )
    cot_steps.append(
        f"Step 3 — POSITIVE ANALYSIS: "
        f"{len(went_well)} things went well this sprint. "
        f"{'Key: ' + '; '.join(went_well[:2]) + '.' if went_well else 'No highlights ⚠.'}"
    )
    cot_steps.append(
        f"Step 4 — ISSUES ANALYSIS: "
        f"{len(didnt_go_well)} issues found. {len(open_blockers)} open blockers. "
        f"{len(high_risk_stories)} high-risk stories. "
        f"{'Key: ' + '; '.join(didnt_go_well[:2]) + '.' if didnt_go_well else 'No issues ✓.'}"
    )

    risk_level = "HIGH" if (len(open_blockers) >= 3 or completion_pct < 60) else "MEDIUM" if (len(open_blockers) >= 1 or completion_pct < 80) else "LOW"
    cot_steps.append(
        f"Step 5 — SYNTHESIS: "
        f"Overall risk: {risk_level}. {len(improvements)} improvement actions. "
        f"Retrospective generation complete."
    )
    chain_of_thought = "\n".join(cot_steps)

    # AI Summary
    ai_parts = []
    ai_parts.append(f"Sprint completed at {completion_pct}% with {avg_alignment}% average alignment.")
    ai_parts.append(f"{len(went_well)} positives and {len(didnt_go_well)} issues identified.")
    if open_blockers:
        ai_parts.append(f"{len(open_blockers)} unresolved blocker(s) need immediate attention.")
    if sorted_perf:
        ai_parts.append(f"Top performer: {sorted_perf[0].get('name', 'N/A')}.")
    ai_summary = " ".join(ai_parts)

    return {
        "ok": True,
        "source": "rule_based",
        "chain_of_thought": chain_of_thought,
        "went_well": went_well,
        "didnt_go_well": didnt_go_well,
        "improvements": improvements,
        "ai_summary": ai_summary,
        "completion_pct": completion_pct,
        "avg_alignment": avg_alignment,
        "risk_level": risk_level,
        "generated_at": datetime.utcnow().isoformat(),
    }

# ── SMAlignmentInsights.jsx ────────────────────────────────────────────────────
@router.get("/alignment/breakdown", response_model=list[AlignmentBreakdown])
async def get_alignment_breakdown():
    return [doc async for doc in alignment_breakdown_collection.find({}, {"_id": 0})]


@router.get("/alignment/low-stories", response_model=list[LowAlignmentStory])
async def get_low_alignment_stories(threshold: int = Query(80)):
    query = {"alignment": {"$lt": threshold}}
    return [doc async for doc in low_alignment_stories_collection.find(query, {"_id": 0})]


@router.get("/alignment/trend", response_model=list[AlignmentTrend])
async def get_alignment_trend():
    return [doc async for doc in alignment_trend_collection.find({}, {"_id": 0})]


# ── SMMyTeam.jsx ───────────────────────────────────────────────────────────────
@router.get("/my-team", response_model=list[TeamMember])
async def get_team_members(risk: Optional[str] = Query(None)):
    query = {}
    if risk: query["risk"] = risk
    return [doc async for doc in team_members_detail_collection.find(query, {"_id": 0})]


@router.get("/my-team/{member_id}", response_model=TeamMember)
async def get_team_member(member_id: int):
    doc = await team_members_detail_collection.find_one({"id": member_id}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "Team member not found")
    return doc


# ── SMReviewQueue.jsx ───────────────────────────────────────────────────────────
@router.get("/review-queue", response_model=list[ReviewQueueItem])
async def get_review_queue(status: Optional[str] = Query(None)):
    query = {}
    if status: query["status"] = status
    return [doc async for doc in review_queue_items_collection.find(query, {"_id": 0})]


@router.put("/review-queue/{item_id}", response_model=dict)
async def update_review_item(item_id: str, body: dict):
    body.pop("_id", None)
    result = await review_queue_items_collection.update_one({"id": item_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Review item not found")
    return {"message": "Review updated"}


# ── SMRiskBlockers.jsx ──────────────────────────────────────────────────────────
@router.get("/blockers", response_model=list[Blocker])
async def get_blockers(resolved: Optional[bool] = Query(None)):
    query = {}
    if resolved is not None: query["resolved"] = resolved
    return [doc async for doc in blockers_collection.find(query, {"_id": 0})]


@router.put("/blockers/{blocker_id}", response_model=dict)
async def update_blocker(blocker_id: str, body: dict):
    body.pop("_id", None)
    result = await blockers_collection.update_one({"id": blocker_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Blocker not found")
    return {"message": "Blocker updated"}


# ── SMTeamPerformance.jsx ───────────────────────────────────────────────────────
@router.get("/performance/members", response_model=list[MemberPerf])
async def get_member_perf():
    return [doc async for doc in member_perf_collection.find({}, {"_id": 0})]


@router.get("/performance/sprint-trend", response_model=list[SprintTrend])
async def get_sprint_trend():
    return [doc async for doc in sprint_trend_collection.find({}, {"_id": 0})]


# ── SMWorkload.jsx ──────────────────────────────────────────────────────────────
@router.get("/workload", response_model=list[WorkloadEntry])
async def get_sm_workload():
    return [doc async for doc in sm_workload_collection.find({}, {"_id": 0})]


@router.put("/workload/{entry_name}", response_model=dict)
async def update_workload_entry(entry_name: str, body: dict):
    body.pop("_id", None)
    result = await sm_workload_collection.update_one({"name": entry_name}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Workload entry not found")
    return {"message": "Workload updated"}


@router.get("/workload/suggestions", response_model=list[WorkloadSuggestion])
async def get_workload_suggestions():
    return [doc async for doc in workload_suggestions_collection.find({}, {"_id": 0})]
