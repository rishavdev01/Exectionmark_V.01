from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.database import (
    incidents_collection, infra_changes_collection,
    logs_alerts_collection, log_ai_analysis_collection,
    devops_tasks_collection, devops_ops_review_collection,
    deployments_collection, pipelines_collection,
    system_health_collection,
)
from app.models.devops_models import Incident, InfraChange, LogAlert, LogAIAnalysis, DevOpsTask

router = APIRouter()


# ── Incidents ──
@router.get("/incidents", response_model=list[Incident])
async def get_incidents(severity: Optional[str] = Query(None)):
    query = {}
    if severity: query["severity"] = severity
    return [doc async for doc in incidents_collection.find(query, {"_id": 0})]


@router.post("/incidents", response_model=dict)
async def create_incident(body: Incident):
    await incidents_collection.insert_one(body.model_dump())
    return {"message": "Incident created"}


# ── Infra Changes ──
@router.get("/infra-changes", response_model=list[InfraChange])
async def get_infra_changes(risk: Optional[str] = Query(None), approved: Optional[bool] = Query(None)):
    query = {}
    if risk: query["risk"] = risk
    if approved is not None: query["approved"] = approved
    return [doc async for doc in infra_changes_collection.find(query, {"_id": 0})]


@router.post("/infra-changes", response_model=dict)
async def create_infra_change(body: InfraChange):
    await infra_changes_collection.insert_one(body.model_dump())
    return {"message": "Change logged"}


# ── Logs & Alerts ──
@router.get("/logs", response_model=list[LogAlert])
async def get_logs(category: Optional[str] = Query(None), severity: Optional[str] = Query(None)):
    query = {}
    if category: query["category"] = category
    if severity: query["severity"] = severity
    return [doc async for doc in logs_alerts_collection.find(query, {"_id": 0})]


@router.get("/logs/ai-analysis", response_model=list[LogAIAnalysis])
async def get_log_ai_analysis():
    return [doc async for doc in log_ai_analysis_collection.find({}, {"_id": 0})]


# ── DevOps Tasks ──
@router.get("/devops-tasks", response_model=list[DevOpsTask])
async def get_devops_tasks(status: Optional[str] = Query(None), type: Optional[str] = Query(None)):
    query = {}
    if status: query["status"] = status
    if type: query["type"] = type
    return [doc async for doc in devops_tasks_collection.find(query, {"_id": 0})]


@router.put("/devops-tasks/{task_id}", response_model=dict)
async def update_devops_task(task_id: str, body: dict):
    body.pop("_id", None)
    result = await devops_tasks_collection.update_one({"id": int(task_id)}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Task not found")
    return {"message": "Updated"}


# ── Ops Reviewer AI Agent (same WEIGHTS as cicd_log_parsing.py) ──
DEVOPS_WEIGHTS = {
    "ci_success": 30,
    "deployment_success": 30,
    "infra_files_changed": 15,
    "monitoring_healthy": 15,
    "no_rollback": 10,
}


def _score_deployment(dep: dict, pipelines: list, incidents: list, infra_changes: list) -> dict:
    """Compute a per-deployment score using the same WEIGHTS as cicd_log_parsing."""
    breakdown = {}
    score = 0

    # ci_success (30 pts) — based on related pipeline CI status
    env = dep.get("environment", "")
    related_pipes = [p for p in pipelines if
                     p.get("environment", "") == env or
                     env.lower() in (p.get("name", "") or "").lower()]
    if related_pipes:
        passed = sum(1 for p in related_pipes if (p.get("status", "") or "").lower() in ("success", "passed", "completed"))
        ci_rate = passed / len(related_pipes) if related_pipes else 0
        pts = int(ci_rate * DEVOPS_WEIGHTS["ci_success"])
        note = f"{passed}/{len(related_pipes)} pipelines passing ({round(ci_rate * 100)}%)"
    else:
        ci_status = dep.get("ciStatus", dep.get("ci_status", dep.get("status", "")))
        if ci_status and ci_status.lower() in ("success", "passed", "completed"):
            pts = DEVOPS_WEIGHTS["ci_success"]
            note = f"CI passed ({ci_status})"
        elif ci_status and ci_status.lower() in ("running", "in_progress"):
            pts = DEVOPS_WEIGHTS["ci_success"] // 2
            note = f"CI in progress ({ci_status})"
        else:
            pts = 0
            note = f"CI failed or unknown ({ci_status})"
    breakdown["ci_success"] = {"max": DEVOPS_WEIGHTS["ci_success"], "earned": pts, "note": note}
    score += pts

    # deployment_success (30 pts) — based on status
    dep_status = (dep.get("status", "") or "").lower()
    if dep_status in ("success", "completed", "active", "live"):
        pts = DEVOPS_WEIGHTS["deployment_success"]
        note = f"Deployment successful ({dep.get('status', '')})"
    elif dep_status in ("running", "in_progress", "deploying"):
        pts = DEVOPS_WEIGHTS["deployment_success"] // 2
        note = f"Deployment in progress ({dep.get('status', '')})"
    elif dep_status == "failed":
        pts = 0
        note = "Deployment failed"
    else:
        pts = DEVOPS_WEIGHTS["deployment_success"] // 3
        note = f"Deployment status: {dep.get('status', 'unknown')}"
    breakdown["deployment_success"] = {"max": DEVOPS_WEIGHTS["deployment_success"], "earned": pts, "note": note}
    score += pts

    # infra_files_changed (15 pts) — are there related infra changes?
    related_infra = [ic for ic in infra_changes if
                     ic.get("environment", "") == env or
                     env.lower() in (ic.get("description", "") or "").lower()]
    if related_infra:
        pts = DEVOPS_WEIGHTS["infra_files_changed"]
        note = f"{len(related_infra)} infra change(s) associated"
    elif infra_changes:
        pts = DEVOPS_WEIGHTS["infra_files_changed"] // 2
        note = f"{len(infra_changes)} infra changes exist (not environment-matched)"
    else:
        pts = 0
        note = "No infra changes detected"
    breakdown["infra_files_changed"] = {"max": DEVOPS_WEIGHTS["infra_files_changed"], "earned": pts, "note": note}
    score += pts

    # monitoring_healthy (15 pts) — based on recent incidents
    related_incidents = [inc for inc in incidents if
                         inc.get("environment", "") == env or
                         (inc.get("severity", "") or "").lower() in ("critical", "high")]
    recent_critical = [inc for inc in related_incidents if (inc.get("severity", "") or "").lower() == "critical"]
    if len(recent_critical) == 0 and len(related_incidents) <= 1:
        pts = DEVOPS_WEIGHTS["monitoring_healthy"]
        note = "Monitoring healthy — no critical incidents"
    elif len(recent_critical) == 0:
        pts = DEVOPS_WEIGHTS["monitoring_healthy"] // 2
        note = f"{len(related_incidents)} incident(s) but none critical"
    else:
        pts = 0
        note = f"{len(recent_critical)} critical incident(s) — monitoring unhealthy"
    breakdown["monitoring_healthy"] = {"max": DEVOPS_WEIGHTS["monitoring_healthy"], "earned": pts, "note": note}
    score += pts

    # no_rollback (10 pts) — no rollback
    has_rollback = dep.get("rollback", False) or "rollback" in (dep.get("notes", "") or "").lower()
    if not has_rollback:
        pts = DEVOPS_WEIGHTS["no_rollback"]
        note = "No rollback ✓"
    else:
        pts = 0
        note = "Rollback detected ⚠"
    breakdown["no_rollback"] = {"max": DEVOPS_WEIGHTS["no_rollback"], "earned": pts, "note": note}
    score += pts

    return {
        "dep_id": dep.get("id", dep.get("_id", "?")),
        "name": dep.get("name", dep.get("service", dep.get("environment", "Deployment"))),
        "environment": env,
        "total_score": min(score, 100),
        "breakdown": breakdown,
    }


@router.post("/generate-ops-review")
async def generate_ops_review():
    """Analyse deployments, pipelines, incidents, and infra changes using DEVOPS_WEIGHTS."""
    deps = [doc async for doc in deployments_collection.find({}, {"_id": 0})]
    pipes = [doc async for doc in pipelines_collection.find({}, {"_id": 0})]
    incidents = [doc async for doc in incidents_collection.find({}, {"_id": 0})]
    infra = [doc async for doc in infra_changes_collection.find({}, {"_id": 0})]
    health = [doc async for doc in system_health_collection.find({}, {"_id": 0})]

    # ── Score each deployment ──
    scorecards = []
    for dep in deps:
        card = _score_deployment(dep, pipes, incidents, infra)
        scorecards.append(card)

    # ── Chain of Thought ──
    cot_lines = [
        f"Step 1 — LOADING DATA: {len(deps)} deployments, {len(pipes)} pipelines, "
        f"{len(incidents)} incidents, {len(infra)} infra changes.",
        f"Step 2 — APPLYING WEIGHTS: ci_success={DEVOPS_WEIGHTS['ci_success']}, "
        f"deployment_success={DEVOPS_WEIGHTS['deployment_success']}, "
        f"infra_files_changed={DEVOPS_WEIGHTS['infra_files_changed']}, "
        f"monitoring_healthy={DEVOPS_WEIGHTS['monitoring_healthy']}, "
        f"no_rollback={DEVOPS_WEIGHTS['no_rollback']}  (Total = 100)",
    ]
    for card in scorecards:
        bd = card["breakdown"]
        parts = [f"{k}={v['earned']}/{v['max']}" for k, v in bd.items()]
        cot_lines.append(
            f"Step 3 — {card['name']} ({card['environment']}): "
            + ", ".join(parts) + f" → Total: {card['total_score']}/100"
        )

    scores = [c["total_score"] for c in scorecards]
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    high_scores = [c for c in scorecards if c["total_score"] >= 70]
    low_scores = [c for c in scorecards if c["total_score"] < 60]

    cot_lines.append(
        f"Step 4 — RELIABILITY SYNTHESIS: Avg score = {avg_score}/100. "
        f"{len(high_scores)} deployment(s) ≥70, {len(low_scores)} deployment(s) <60."
    )
    chain_of_thought = "\n".join(cot_lines)

    # ── Good Practices ──
    good_practices = []
    successful_deps = [c for c in scorecards if c["breakdown"]["deployment_success"]["earned"] >= 25]
    if successful_deps:
        good_practices.append(f"{len(successful_deps)} deployment(s) completed successfully — strong delivery pipeline.")
    healthy_monitoring = [c for c in scorecards if c["breakdown"]["monitoring_healthy"]["earned"] == DEVOPS_WEIGHTS["monitoring_healthy"]]
    if healthy_monitoring:
        good_practices.append(f"{len(healthy_monitoring)} environment(s) with clean monitoring — no critical incidents.")
    no_rollbacks = [c for c in scorecards if c["breakdown"]["no_rollback"]["earned"] > 0]
    if no_rollbacks:
        good_practices.append(f"{len(no_rollbacks)}/{len(scorecards)} deployment(s) with zero rollbacks.")
    if not good_practices:
        good_practices = ["Operations running within expected parameters.", "Infrastructure changes follow approval workflow."]

    # ── Issues Found ──
    issues = []
    for c in scorecards:
        bd = c["breakdown"]
        if bd["ci_success"]["earned"] < 15:
            issues.append(f"{c['name']} ({c['environment']}) — CI issues: {bd['ci_success']['note']}")
        if bd["deployment_success"]["earned"] == 0:
            issues.append(f"{c['name']} — Deployment failed. Blocking release pipeline.")
        if bd["monitoring_healthy"]["earned"] == 0:
            issues.append(f"{c['name']} — {bd['monitoring_healthy']['note']}")
        if bd["no_rollback"]["earned"] == 0:
            issues.append(f"{c['name']} — {bd['no_rollback']['note']}")
    critical_incidents = [inc for inc in incidents if (inc.get("severity", "") or "").lower() == "critical"]
    if critical_incidents:
        issues.append(f"{len(critical_incidents)} critical incident(s) open — requires immediate attention.")
    high_risk_infra = [ic for ic in infra if (ic.get("risk", "") or "").lower() == "high"]
    if high_risk_infra:
        issues.append(f"{len(high_risk_infra)} high-risk infrastructure change(s) detected.")
    if not issues:
        issues = ["No critical issues detected. All systems operational."]

    # ── Action Items ──
    actions = []
    for c in low_scores:
        bd = c["breakdown"]
        dep_author = next((d.get("author", d.get("deployer", "DevOps")) for d in deps
                           if d.get("id") == c["dep_id"] or d.get("name") == c["name"]), "DevOps")
        if bd["ci_success"]["earned"] < 15:
            actions.append({
                "action": f"Fix CI failures for {c['name']} ({c['environment']})",
                "assignee": dep_author, "deadline": "Today", "priority": "High"
            })
        if bd["deployment_success"]["earned"] == 0:
            actions.append({
                "action": f"Investigate failed deployment: {c['name']}",
                "assignee": dep_author, "deadline": "Today", "priority": "Critical"
            })
        if bd["no_rollback"]["earned"] == 0:
            actions.append({
                "action": f"Analyse rollback on {c['name']} — identify root cause",
                "assignee": dep_author, "deadline": "2 days", "priority": "High"
            })
    for inc in critical_incidents:
        actions.append({
            "action": f"Resolve critical incident: {inc.get('title', inc.get('id', 'Unknown'))}",
            "assignee": inc.get("assignee", "On-Call"), "deadline": "ASAP", "priority": "Critical"
        })
    if not actions:
        actions.append({
            "action": "Continue monitoring deployment health",
            "assignee": "DevOps Team", "deadline": "Ongoing", "priority": "Low"
        })

    # ── AI Summary ──
    ai_summary = (
        f"Ops Review ({len(deps)} deployments, {len(pipes)} pipelines): "
        f"Average score {avg_score}/100 using 5-factor WEIGHTS "
        f"(ci_success={DEVOPS_WEIGHTS['ci_success']}, deployment={DEVOPS_WEIGHTS['deployment_success']}, "
        f"infra={DEVOPS_WEIGHTS['infra_files_changed']}, monitoring={DEVOPS_WEIGHTS['monitoring_healthy']}, "
        f"no_rollback={DEVOPS_WEIGHTS['no_rollback']}). "
        f"{len(high_scores)} deployment(s) scored ≥70. "
        f"{'⚠ ' + str(len(low_scores)) + ' deployment(s) scored <60 — needs attention. ' if low_scores else ''}"
        f"{'Critical incidents: ' + str(len(critical_incidents)) + '. ' if critical_incidents else ''}"
        f"Overall ops health: {'strong' if avg_score >= 75 else 'moderate' if avg_score >= 55 else 'needs improvement'}."
    )

    # Load cached ops review data
    cached = await devops_ops_review_collection.find_one({}, {"_id": 0})

    result = {
        "ok": True,
        "source": "rule_based",
        "weights": DEVOPS_WEIGHTS,
        "scorecards": scorecards,
        "avg_score": avg_score,
        "good_practices": good_practices,
        "issues_found": issues,
        "action_items": actions,
        "ai_summary": ai_summary,
        "chain_of_thought": chain_of_thought,
    }

    # Cache result
    await devops_ops_review_collection.update_one(
        {}, {"$set": result}, upsert=True
    )

    return result


# ── Get cached ops review ──
@router.get("/ops-review")
async def get_ops_review():
    doc = await devops_ops_review_collection.find_one({}, {"_id": 0})
    return doc if doc else {}


# ── DevOps Task Workflow (mark-done) ──
from pydantic import BaseModel
from datetime import datetime


class DevOpsMarkDoneRequest(BaseModel):
    markedBy: str = ""


@router.post("/devops-tasks/{task_id}/mark-done")
async def mark_devops_task_done(task_id: str, body: DevOpsMarkDoneRequest = DevOpsMarkDoneRequest()):
    """
    DevOps marks task as done → AI agent reviews CI alignment → status becomes 'In Review'.
    """
    task = await devops_tasks_collection.find_one({"id": int(task_id)}, {"_id": 0})
    if not task:
        raise HTTPException(404, "DevOps task not found")

    # ── AI Agent review ──
    review_notes = []
    alignment = task.get("alignment", 0)

    if task.get("ciAligned"):
        review_notes.append("✅ CI logs aligned with task.")
    else:
        review_notes.append("⚠️ CI logs NOT aligned — review required.")

    if task.get("deployTriggered"):
        review_notes.append("✅ Deployment triggered successfully.")
    else:
        review_notes.append("⚠️ Deployment NOT triggered — manual follow-up needed.")

    if task.get("filesCorrect"):
        review_notes.append("✅ Correct files modified.")
    else:
        review_notes.append("🔴 Unexpected file changes detected — possible scope drift.")

    if alignment >= 80:
        review_notes.append(f"✅ High alignment ({alignment}%).")
    elif alignment >= 60:
        review_notes.append(f"⚠️ Moderate alignment ({alignment}%).")
    else:
        review_notes.append(f"🔴 Low alignment ({alignment}%) — review carefully.")

    review_notes.append(f"Task '{task.get('story', '')}' marked done by {body.markedBy or 'DevOps'}. Awaiting Lead approval.")

    now = datetime.utcnow().isoformat()
    update_data = {
        "status": "In Review",
        "reviewedBy": "AI Agent",
        "reviewNotes": " | ".join(review_notes),
        "reviewedAt": now,
    }

    await devops_tasks_collection.update_one({"id": int(task_id)}, {"$set": update_data})
    updated = await devops_tasks_collection.find_one({"id": int(task_id)}, {"_id": 0})

    return {
        "message": "DevOps task marked as done — now In Review",
        "task": updated,
        "review": {
            "reviewedBy": "AI Agent",
            "notes": review_notes,
            "reviewedAt": now,
        }
    }
