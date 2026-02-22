from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.database import (
    pull_requests_collection, branches_collection, submissions_collection,
    dev_ai_feedback_collection, dev_progress_history_collection,
)
from app.models.dev_models import PullRequest, Branch, Submission

router = APIRouter()


# ── Pull Requests ──
@router.get("/pull-requests", response_model=list[PullRequest])
async def get_pull_requests(sprint: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    query = {}
    if sprint: query["sprint"] = sprint
    if status: query["status"] = status
    return [doc async for doc in pull_requests_collection.find(query, {"_id": 0})]


@router.post("/pull-requests", response_model=dict)
async def create_pull_request(body: PullRequest):
    await pull_requests_collection.insert_one(body.model_dump())
    return {"message": "Pull request created"}


@router.put("/pull-requests/{pr_id}", response_model=dict)
async def update_pull_request(pr_id: str, body: dict):
    body.pop("_id", None)
    result = await pull_requests_collection.update_one({"id": pr_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "PR not found")
    return {"message": "Updated"}


# ── Branches ──
@router.get("/branches", response_model=list[Branch])
async def get_branches(sprint: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    query = {}
    if sprint: query["sprint"] = sprint
    if status: query["status"] = status
    return [doc async for doc in branches_collection.find(query, {"_id": 0})]


# ── Submissions ──
@router.get("/submissions", response_model=list[Submission])
async def get_submissions(tab: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    query = {}
    if tab: query["tab"] = tab
    if status: query["status"] = status
    return [doc async for doc in submissions_collection.find(query, {"_id": 0})]


@router.post("/submissions", response_model=dict)
async def create_submission(body: Submission):
    await submissions_collection.insert_one(body.model_dump())
    return {"message": "Submission created"}


@router.put("/submissions/{sub_id}", response_model=dict)
async def update_submission(sub_id: str, body: dict):
    body.pop("_id", None)
    result = await submissions_collection.update_one({"id": sub_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Submission not found")
    return {"message": "Updated"}


# ── AI Feedback ──
FALLBACK_AI_FEEDBACK = {
    "alignment_data": [
        {"metric": "Keyword Match", "value": 87, "color": "#3b82f6"},
        {"metric": "File Path Relevance", "value": 79, "color": "#8b5cf6"},
        {"metric": "Semantic Similarity", "value": 83, "color": "#06b6d4"},
        {"metric": "Scope Drift", "value": 14, "color": "#ef4444", "invert": True},
    ],
    "suggestions": [
        {"text": "Consider splitting PR #345 into smaller units for faster review cycles.", "priority": "High"},
        {"text": "Avoid modifying unrelated UI files in backend-focused branches.", "priority": "High"},
        {"text": "Add unit tests for payment service — current coverage is 72%, target is 85%.", "priority": "Medium"},
        {"text": "Externalize retry backoff configuration instead of hardcoding values.", "priority": "Low"},
        {"text": "Consider adding Redis fallback strategy for rate limiting middleware.", "priority": "Medium"},
        {"text": "Database migration scripts should always include a rollback plan.", "priority": "High"},
    ],
}


@router.get("/ai-feedback")
async def get_ai_feedback():
    doc = await dev_ai_feedback_collection.find_one({}, {"_id": 0})
    return doc if doc else FALLBACK_AI_FEEDBACK


# ── Progress History ──
FALLBACK_PROGRESS_HISTORY = [
    {"sprint": "Sprint 8", "tasksCompleted": 8, "storiesDelivered": 3, "avgCycleTime": "2.1d", "bugs": 1, "prsRaised": 4, "score": 78},
    {"sprint": "Sprint 9", "tasksCompleted": 11, "storiesDelivered": 4, "avgCycleTime": "1.8d", "bugs": 0, "prsRaised": 5, "score": 85},
    {"sprint": "Sprint 10", "tasksCompleted": 7, "storiesDelivered": 2, "avgCycleTime": "2.4d", "bugs": 2, "prsRaised": 3, "score": 70},
    {"sprint": "Sprint 11", "tasksCompleted": 10, "storiesDelivered": 4, "avgCycleTime": "1.9d", "bugs": 1, "prsRaised": 6, "score": 82},
    {"sprint": "Sprint 12", "tasksCompleted": 9, "storiesDelivered": 3, "avgCycleTime": "2.0d", "bugs": 0, "prsRaised": 5, "score": 80},
]


@router.get("/progress-history")
async def get_progress_history():
    docs = [doc async for doc in dev_progress_history_collection.find({}, {"_id": 0})]
    return docs if docs else FALLBACK_PROGRESS_HISTORY


# ── Code Review Agent (same WEIGHTS as github_code_analysis.py) ──
WEIGHTS = {
    "branch_created": 10,
    "commits_pushed": 20,
    "pr_created": 20,
    "pr_reviewed": 15,
    "pr_merged": 20,
    "file_alignment": 15,
}


def _score_pr(pr: dict, branch: dict | None) -> dict:
    """Compute a per-PR score using the same WEIGHTS as github_code_analysis."""
    breakdown = {}
    score = 0

    # branch_created (10 pts) — matching branch exists
    has_branch = branch is not None
    pts = WEIGHTS["branch_created"] if has_branch else 0
    breakdown["branch_created"] = {"max": WEIGHTS["branch_created"], "earned": pts,
                                    "note": f"Branch '{branch['name']}' exists" if has_branch else "No matching branch found"}
    score += pts

    # commits_pushed (20 pts) — 4 pts per commit, max 5 commits
    commit_count = branch.get("commits", 0) if branch else 0
    pts = min(commit_count * 4, WEIGHTS["commits_pushed"])
    breakdown["commits_pushed"] = {"max": WEIGHTS["commits_pushed"], "earned": pts,
                                    "note": f"{commit_count} commit(s) — {pts}/{WEIGHTS['commits_pushed']} pts"}
    score += pts

    # pr_created (20 pts) — PR exists
    pts = WEIGHTS["pr_created"]  # we know the PR exists since we're iterating PRs
    breakdown["pr_created"] = {"max": WEIGHTS["pr_created"], "earned": pts,
                                "note": f"{pr['id']} created"}
    score += pts

    # pr_reviewed (15 pts) — Approved = full, in review/changes = half
    review_status = pr.get("reviewStatus", "Open")
    if review_status == "Approved":
        pts = WEIGHTS["pr_reviewed"]
        note = "Approved — full credit"
    elif review_status in ("In Review", "Changes Requested"):
        pts = WEIGHTS["pr_reviewed"] // 2
        note = f"{review_status} — partial credit ({pts}/{WEIGHTS['pr_reviewed']})"
    else:
        pts = 0
        note = f"Not reviewed yet ({review_status})"
    breakdown["pr_reviewed"] = {"max": WEIGHTS["pr_reviewed"], "earned": pts, "note": note}
    score += pts

    # pr_merged (20 pts) — Only if Merged
    is_merged = pr.get("status", "").lower() == "merged"
    pts = WEIGHTS["pr_merged"] if is_merged else 0
    breakdown["pr_merged"] = {"max": WEIGHTS["pr_merged"], "earned": pts,
                               "note": "Merged ✓" if is_merged else "Not merged yet"}
    score += pts

    # file_alignment (15 pts) — from pr.alignment (0–100) or branch aiRelevance
    raw_alignment = pr.get("alignment", 0) or (branch.get("aiRelevance", 0) if branch else 0)
    alignment_fraction = raw_alignment / 100.0
    pts = int(alignment_fraction * WEIGHTS["file_alignment"])
    breakdown["file_alignment"] = {"max": WEIGHTS["file_alignment"], "earned": pts,
                                    "note": f"Alignment {raw_alignment}% → {pts}/{WEIGHTS['file_alignment']} pts"}
    score += pts

    return {
        "pr_id": pr["id"],
        "title": pr.get("title", ""),
        "total_score": min(score, 100),
        "breakdown": breakdown,
    }


@router.post("/generate-code-review")
async def generate_code_review():
    """Analyse PRs and branches using the same WEIGHTS scoring as github_code_analysis."""
    prs = [doc async for doc in pull_requests_collection.find({}, {"_id": 0})]
    branches_list = [doc async for doc in branches_collection.find({}, {"_id": 0})]

    # Map branch name to branch doc for quick lookup
    branch_map = {}
    for b in branches_list:
        branch_map[b["name"]] = b

    # ── Score each PR ──
    scorecards = []
    for pr in prs:
        # Try to match PR branch to a branch doc
        matched_branch = branch_map.get(pr.get("branch", ""))
        card = _score_pr(pr, matched_branch)
        scorecards.append(card)

    # ── Chain of Thought (per-step reasoning) ──
    cot_lines = [
        f"Step 1 — LOADING DATA: Found {len(prs)} pull requests and {len(branches_list)} active branches.",
        f"Step 2 — APPLYING WEIGHTS: branch_created={WEIGHTS['branch_created']}, commits_pushed={WEIGHTS['commits_pushed']}, "
        f"pr_created={WEIGHTS['pr_created']}, pr_reviewed={WEIGHTS['pr_reviewed']}, pr_merged={WEIGHTS['pr_merged']}, "
        f"file_alignment={WEIGHTS['file_alignment']}  (Total = 100)",
    ]

    for card in scorecards:
        bd = card["breakdown"]
        line = f"Step 3 — {card['pr_id']} ({card['title']}): "
        parts = [f"{k}={v['earned']}/{v['max']}" for k, v in bd.items()]
        line += ", ".join(parts) + f" → Total: {card['total_score']}/100"
        cot_lines.append(line)

    # Aggregate stats
    scores = [c["total_score"] for c in scorecards]
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    high_scores = [c for c in scorecards if c["total_score"] >= 70]
    low_scores = [c for c in scorecards if c["total_score"] < 60]

    cot_lines.append(
        f"Step 4 — RISK SYNTHESIS: Average score = {avg_score}/100. "
        f"{len(high_scores)} PR(s) ≥70, {len(low_scores)} PR(s) <60. "
        f"Generating recommendations."
    )
    chain_of_thought = "\n".join(cot_lines)

    # ── Good Practices ──
    good_practices = []
    fully_reviewed = [c for c in scorecards if c["breakdown"]["pr_reviewed"]["earned"] == WEIGHTS["pr_reviewed"]]
    if fully_reviewed:
        good_practices.append(f"{len(fully_reviewed)} PR(s) fully reviewed and approved — strong review discipline.")
    high_align = [c for c in scorecards if c["breakdown"]["file_alignment"]["earned"] >= 12]
    if high_align:
        good_practices.append(f"{len(high_align)} PR(s) have high file alignment (≥80%) — changes are well-scoped.")
    merged_prs = [c for c in scorecards if c["breakdown"]["pr_merged"]["earned"] > 0]
    if merged_prs:
        good_practices.append(f"{len(merged_prs)} PR(s) successfully merged — delivery pipeline flowing.")
    if not good_practices:
        good_practices = ["Code submissions are generally well-structured.", "Branch naming follows team conventions."]

    # ── Issues Found ──
    issues = []
    for c in scorecards:
        bd = c["breakdown"]
        if bd["file_alignment"]["earned"] < 10:
            issues.append(f"{c['pr_id']} — File alignment low ({bd['file_alignment']['note']}). Possible scope drift.")
        if bd["commits_pushed"]["earned"] < 8:
            issues.append(f"{c['pr_id']} — Low commit activity ({bd['commits_pushed']['note']}). Progress may be stalled.")
        if bd["pr_reviewed"]["earned"] == 0:
            issues.append(f"{c['pr_id']} — Not reviewed yet. Blocking merge pipeline.")
    conflict_branches = [b for b in branches_list if b.get("conflicts")]
    for b in conflict_branches:
        issues.append(f"Branch '{b['name']}' has merge conflicts — {b.get('aiNote', 'Needs resolution')}")
    failing_ci = [p for p in prs if p.get("ci") == "Fail"]
    for p in failing_ci:
        issues.append(f"{p['id']} CI failing — blocking merge.")
    if not issues:
        issues = ["No critical issues detected. All PRs look healthy."]

    # ── Action Items ──
    actions = []
    for c in low_scores:
        bd = c["breakdown"]
        if bd["file_alignment"]["earned"] < 10:
            actions.append({
                "action": f"Refactor {c['pr_id']} — reduce out-of-scope changes (alignment {bd['file_alignment']['note']})",
                "assignee": next((p.get("author", "Dev") for p in prs if p["id"] == c["pr_id"]), "Dev"),
                "deadline": "This Sprint",
                "priority": "High"
            })
        if bd["pr_reviewed"]["earned"] == 0:
            actions.append({
                "action": f"Request code review for {c['pr_id']}",
                "assignee": next((p.get("author", "Dev") for p in prs if p["id"] == c["pr_id"]), "Dev"),
                "deadline": "2 days",
                "priority": "High"
            })
    for b in conflict_branches:
        actions.append({
            "action": f"Resolve merge conflicts on '{b['name']}'",
            "assignee": b.get("author", "Developer"),
            "deadline": "2 days",
            "priority": "High"
        })
    for p in failing_ci:
        actions.append({
            "action": f"Fix CI failures on {p['id']}",
            "assignee": p.get("author", "Developer"),
            "deadline": "Today",
            "priority": "High"
        })
    if not actions:
        actions.append({
            "action": "Continue monitoring PR scores",
            "assignee": "Team",
            "deadline": "Ongoing",
            "priority": "Low"
        })

    # ── AI Summary ──
    ai_summary = (
        f"Sprint Code Review ({len(prs)} PRs, {len(branches_list)} branches): "
        f"Average score {avg_score}/100 using 6-factor WEIGHTS "
        f"(branch_created={WEIGHTS['branch_created']}, commits={WEIGHTS['commits_pushed']}, "
        f"pr_created={WEIGHTS['pr_created']}, reviewed={WEIGHTS['pr_reviewed']}, "
        f"merged={WEIGHTS['pr_merged']}, alignment={WEIGHTS['file_alignment']}). "
        f"{len(high_scores)} PR(s) scored ≥70. "
        f"{'⚠ ' + str(len(low_scores)) + ' PR(s) scored <60 — needs attention. ' if low_scores else ''}"
        f"{'CI failing on ' + str(len(failing_ci)) + ' PR(s). ' if failing_ci else ''}"
        f"{'Merge conflicts on ' + str(len(conflict_branches)) + ' branch(es). ' if conflict_branches else ''}"
        f"Overall code quality: {'strong' if avg_score >= 75 else 'moderate' if avg_score >= 55 else 'needs improvement'}."
    )

    result = {
        "ok": True,
        "source": "rule_based",
        "weights": WEIGHTS,
        "scorecards": scorecards,
        "avg_score": avg_score,
        "good_practices": good_practices,
        "issues_found": issues,
        "action_items": actions,
        "ai_summary": ai_summary,
        "chain_of_thought": chain_of_thought,
    }

    # Cache result
    await dev_ai_feedback_collection.update_one(
        {}, {"$set": {"code_review": result}}, upsert=True
    )

    return result

