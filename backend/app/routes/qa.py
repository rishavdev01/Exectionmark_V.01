from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.database import (
    test_cases_collection, bugs_qa_collection, assigned_stories_collection,
    regression_collection, release_checks_collection, blocking_bugs_collection,
    quality_metrics_collection, test_runs_collection, qa_reports_collection,
)
from app.models.qa_models import (
    TestCase, Bug, AssignedStory, RegressionSuite,
    ReleaseCheck, BlockingBug, QualityMetric, TestRun, QAReport,
)

router = APIRouter()


# ── Test Cases ──
@router.get("/test-cases", response_model=list[TestCase])
async def get_test_cases(status: Optional[str] = Query(None), priority: Optional[str] = Query(None)):
    query = {}
    if status: query["status"] = status
    if priority: query["priority"] = priority
    return [doc async for doc in test_cases_collection.find(query, {"_id": 0})]


@router.post("/test-cases", response_model=dict)
async def create_test_case(body: TestCase):
    await test_cases_collection.insert_one(body.model_dump())
    return {"message": "Test case created"}


@router.put("/test-cases/{tc_id}", response_model=dict)
async def update_test_case(tc_id: str, body: dict):
    body.pop("_id", None)
    result = await test_cases_collection.update_one({"id": tc_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Test case not found")
    return {"message": "Updated"}


@router.delete("/test-cases/{tc_id}", response_model=dict)
async def delete_test_case(tc_id: str):
    await test_cases_collection.delete_one({"id": tc_id})
    return {"message": "Deleted"}


# ── Bugs (QA) ──
@router.get("/bugs-qa", response_model=list[Bug])
async def get_bugs_qa(severity: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    query = {}
    if severity: query["severity"] = severity
    if status: query["status"] = status
    return [doc async for doc in bugs_qa_collection.find(query, {"_id": 0})]


@router.post("/bugs-qa", response_model=dict)
async def create_bug(body: Bug):
    await bugs_qa_collection.insert_one(body.model_dump())
    return {"message": "Bug created"}


@router.put("/bugs-qa/{bug_id}", response_model=dict)
async def update_bug(bug_id: str, body: dict):
    body.pop("_id", None)
    result = await bugs_qa_collection.update_one({"id": bug_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Bug not found")
    return {"message": "Updated"}


# ── Assigned Stories ──
@router.get("/assigned-stories", response_model=list[AssignedStory])
async def get_assigned_stories(testStatus: Optional[str] = Query(None)):
    query = {}
    if testStatus: query["testStatus"] = testStatus
    return [doc async for doc in assigned_stories_collection.find(query, {"_id": 0})]


# ── Regression Suite ──
@router.get("/regression", response_model=list[RegressionSuite])
async def get_regression_suites():
    return [doc async for doc in regression_collection.find({}, {"_id": 0})]


# ── Release Checks ──
@router.get("/release-checks", response_model=list[ReleaseCheck])
async def get_release_checks():
    return [doc async for doc in release_checks_collection.find({}, {"_id": 0})]


@router.get("/blocking-bugs", response_model=list[BlockingBug])
async def get_blocking_bugs():
    return [doc async for doc in blocking_bugs_collection.find({}, {"_id": 0})]


# ── Quality Metrics ──
@router.get("/quality-metrics", response_model=list[QualityMetric])
async def get_quality_metrics():
    return [doc async for doc in quality_metrics_collection.find({}, {"_id": 0})]


# ── Test Runs ──
@router.get("/test-runs", response_model=list[TestRun])
async def get_test_runs():
    return [doc async for doc in test_runs_collection.find({}, {"_id": 0})]


# ── QA Reports ──
FALLBACK_REPORTS = [
    {
        "id": 1, "name": "Sprint QA Report", "color": "#3b82f6", "category": "Sprint",
        "description": "Comprehensive QA summary for the current sprint including test results, bug counts, and quality scores.",
        "lastGenerated": "Feb 20, 2026",
        "data": [{"label": "Tests Run", "value": "271"}, {"label": "Pass Rate", "value": "91%"}, {"label": "Bugs Found", "value": "8"}, {"label": "Quality Score", "value": "85%"}]
    },
    {
        "id": 2, "name": "Bug Trend Report", "color": "#ef4444", "category": "Bugs",
        "description": "Analysis of bug discovery and resolution trends across recent sprints. Highlights repeat defects.",
        "lastGenerated": "Feb 20, 2026",
        "data": [{"label": "New Bugs", "value": "8"}, {"label": "Resolved", "value": "14"}, {"label": "Reopened", "value": "3"}, {"label": "Net Change", "value": "-6"}]
    },
    {
        "id": 3, "name": "Release Quality Report", "color": "#10b981", "category": "Release",
        "description": "Pre-release quality assessment including blocking bugs, regression results, and AI risk verdict.",
        "lastGenerated": "Feb 19, 2026",
        "data": [{"label": "Risk Level", "value": "Medium"}, {"label": "Blockers", "value": "5"}, {"label": "Regression Pass", "value": "86%"}, {"label": "Coverage", "value": "82%"}]
    },
    {
        "id": 4, "name": "Regression Stability Report", "color": "#8b5cf6", "category": "Regression",
        "description": "Stability analysis of regression suite across sprints with flaky test detection and module-level breakdown.",
        "lastGenerated": "Feb 20, 2026",
        "data": [{"label": "Total Cases", "value": "86"}, {"label": "Pass Rate", "value": "86%"}, {"label": "Flaky Tests", "value": "2"}, {"label": "Stable Modules", "value": "4/6"}]
    },
]


@router.get("/reports", response_model=list[QAReport])
async def get_qa_reports():
    docs = [doc async for doc in qa_reports_collection.find({}, {"_id": 0})]
    return docs if docs else FALLBACK_REPORTS
