"""
Dashboard route — aggregated data per role
Each endpoint returns pre-shaped data matching the role's dashboard component.
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.database import (
    users_collection,
    employees_collection,
    sprints_collection,
    stories_collection,
    tasks_collection,
    projects_collection,
    candidates_collection,
    pipelines_collection,
    deployments_collection,
    system_health_collection,
    alerts_collection,
    bugs_collection,
    review_queue_collection,
    escalations_collection,
)

router = APIRouter()


@router.get("/ceo")
async def ceo_dashboard():
    """Aggregated data for CEODashboard.jsx"""
    total_tasks = await tasks_collection.count_documents({})
    completed_tasks = await tasks_collection.count_documents({"status": "Done"})
    total_sprints = await sprints_collection.count_documents({})
    active_sprints = await sprints_collection.count_documents({"status": {"$in": ["Active", "In Progress"]}})
    open_escalations = await escalations_collection.count_documents({"status": {"$ne": "Resolved"}})
    total_employees = await employees_collection.count_documents({})
    total_projects = await projects_collection.count_documents({})

    # Recent escalations
    escalations = []
    async for e in escalations_collection.find({"status": {"$ne": "Resolved"}}, {"_id": 0}).limit(5):
        escalations.append(e)

    return {
        "stats": {
            "totalTasks": total_tasks,
            "completedTasks": completed_tasks,
            "totalSprints": total_sprints,
            "activeSprints": active_sprints,
            "openEscalations": open_escalations,
            "totalEmployees": total_employees,
            "totalProjects": total_projects,
            "executionRate": round(completed_tasks / total_tasks * 100, 1) if total_tasks else 0,
        },
        "recentEscalations": escalations,
    }


@router.get("/pm")
async def pm_dashboard():
    """Aggregated data for PMDashboard.jsx"""
    total_stories = await stories_collection.count_documents({})
    stories_by_status = {}
    for status in ["To Do", "In Progress", "In Review", "Done"]:
        stories_by_status[status] = await stories_collection.count_documents({"status": status})

    pending_approvals = await review_queue_collection.count_documents({"leadApproval": "Pending"})

    # Sprint progress
    sprints = []
    async for s in sprints_collection.find({}, {"_id": 0, "name": 1, "completion": 1, "totalStories": 1}):
        sprints.append({"name": s.get("name"), "progress": s.get("completion", 0), "tasks": s.get("totalStories", 0)})

    return {
        "stats": {
            "activeSprints": await sprints_collection.count_documents({"status": {"$in": ["Active", "In Progress"]}}),
            "totalTasks": total_stories,
            "pendingApprovals": pending_approvals,
            "sprintVelocity": 87,
        },
        "taskDistribution": [
            {"name": k, "value": v, "color": {"To Do": "#6b7280", "In Progress": "#3b82f6", "In Review": "#f59e0b", "Done": "#10b981"}[k]}
            for k, v in stories_by_status.items()
        ],
        "sprintProgress": sprints,
    }


@router.get("/lead")
async def lead_dashboard():
    """Aggregated data for LeadDashboard.jsx"""
    employees = []
    async for e in employees_collection.find({}, {"_id": 0}).limit(10):
        employees.append(e)

    review_items = []
    async for r in review_queue_collection.find({}, {"_id": 0}).limit(5):
        review_items.append(r)

    return {
        "stats": {
            "teamMembers": len(employees),
            "activeTasks": 32,
            "reviewQueue": len(review_items),
            "teamPerformance": 88,
        },
        "teamMembers": employees,
        "reviewQueue": review_items,
    }


@router.get("/developer")
async def developer_dashboard(user_name: Optional[str] = Query(None)):
    """Aggregated data for DevDashboard.jsx"""
    query = {}
    if user_name:
        query["to_user"] = user_name

    tasks = []
    async for t in tasks_collection.find(query, {"_id": 0}).limit(10):
        tasks.append(t)

    return {
        "stats": {
            "activeTasks": len(tasks),
            "activeBranches": 3,
            "pullRequests": 3,
            "aiQualityScore": 92,
        },
        "myTasks": tasks,
    }


@router.get("/devops")
async def devops_dashboard():
    """Aggregated data for DevOpsDashboard.jsx"""
    pipelines = []
    async for p in pipelines_collection.find({}, {"_id": 0}):
        pipelines.append(p)

    deps = []
    async for d in deployments_collection.find({}, {"_id": 0}):
        deps.append(d)

    health = []
    async for h in system_health_collection.find({}, {"_id": 0}):
        health.append(h)

    logs = []
    async for a in alerts_collection.find({}, {"_id": 0}).limit(5):
        logs.append(a)

    return {
        "stats": {
            "pipelines": len(pipelines),
            "recentDeployments": len(deps),
            "servicesMonitored": len(health),
            "avgUptime": "99.9%",
        },
        "pipelines": pipelines,
        "deployments": deps,
        "health_data": health,
        "alerts": logs,
    }


@router.get("/qa")
async def qa_dashboard():
    """Aggregated data for QADashboard.jsx"""
    open_bugs = await bugs_collection.count_documents({"status": "Open"})
    total_bugs = await bugs_collection.count_documents({})

    bugs_by_status = []
    for status, color in [("Open", "#ef4444"), ("In Progress", "#f59e0b"), ("Resolved", "#10b981"), ("Reopened", "#8b5cf6")]:
        count = await bugs_collection.count_documents({"status": status})
        bugs_by_status.append({"name": status, "value": count, "color": color})

    return {
        "stats": {
            "assignedStories": 12,
            "totalTestCases": 86,
            "openBugs": open_bugs,
            "qualityScore": 85,
        },
        "bugsByStatus": bugs_by_status,
    }


@router.get("/hr")
async def hr_dashboard():
    """Aggregated data for HRDashboard.jsx"""
    total_employees = await employees_collection.count_documents({})
    total_candidates = await candidates_collection.count_documents({})
    pending_invitations = await candidates_collection.count_documents({"status": "Pending"})

    recent_candidates = []
    async for c in candidates_collection.find({}, {"_id": 0}).limit(5):
        recent_candidates.append(c)

    return {
        "stats": {
            "totalEmployees": total_employees,
            "totalInvitations": total_candidates,
            "pendingInvitations": pending_invitations,
            "onboarding": 3,
        },
        "recentInvitations": recent_candidates,
    }
