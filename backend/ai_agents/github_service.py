"""
GitHub API Service — async client using httpx + developer PAT token.

Provides methods to query branches, commits, PRs, reviews, and
file changes from the GitHub REST API v3.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import httpx

GITHUB_API = "https://api.github.com"


def _headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


# ── Branch ───────────────────────────────────────────────────────
async def check_branch(
    token: str, owner: str, repo: str, branch: str
) -> dict[str, Any]:
    """Check if a branch exists and return last commit info."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/branches/{branch}"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token))
    if r.status_code == 404:
        return {"exists": False, "last_commit_date": None, "commit_sha": None}
    r.raise_for_status()
    data = r.json()
    commit = data.get("commit", {})
    commit_date = (
        commit.get("commit", {}).get("committer", {}).get("date")
    )
    return {
        "exists": True,
        "last_commit_date": commit_date,
        "commit_sha": commit.get("sha"),
    }


# ── Commits by author ────────────────────────────────────────────
async def get_commits(
    token: str,
    owner: str,
    repo: str,
    branch: str,
    author: str,
    since: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Return commits by a specific author on a branch."""
    params: dict[str, str] = {"sha": branch, "author": author, "per_page": "100"}
    if since:
        params["since"] = since
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token), params=params)
    if r.status_code == 404:
        return []
    r.raise_for_status()

    commits = []
    for c in r.json():
        commits.append({
            "sha": c["sha"],
            "message": c["commit"]["message"],
            "date": c["commit"]["committer"]["date"],
            "author": c["commit"]["author"]["name"],
        })
    return commits


# ── Pull Requests ────────────────────────────────────────────────
async def get_pull_requests(
    token: str,
    owner: str,
    repo: str,
    head_branch: str,
    state: str = "all",
) -> list[dict[str, Any]]:
    """Return PRs whose head branch matches the expected branch."""
    params = {"state": state, "per_page": "100"}
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token), params=params)
    if r.status_code == 404:
        return []
    r.raise_for_status()

    prs = []
    for pr in r.json():
        pr_head = pr.get("head", {}).get("ref", "")
        if pr_head != head_branch:
            continue
        prs.append({
            "pr_number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "created_at": pr["created_at"],
            "merged_at": pr.get("merged_at"),
            "comments": pr.get("comments", 0),
            "review_comments": pr.get("review_comments", 0),
        })
    return prs


# ── PR Files Changed ─────────────────────────────────────────────
async def get_pr_files(
    token: str, owner: str, repo: str, pr_number: int
) -> list[dict[str, Any]]:
    """Return files changed in a PR."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token))
    r.raise_for_status()

    files = []
    for f in r.json():
        files.append({
            "filename": f["filename"],
            "status": f["status"],  # added | modified | removed
            "additions": f["additions"],
            "deletions": f["deletions"],
            "changes": f["changes"],
        })
    return files


# ── PR Reviews ───────────────────────────────────────────────────
async def get_pr_reviews(
    token: str, owner: str, repo: str, pr_number: int
) -> list[dict[str, Any]]:
    """Return reviews on a PR."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token))
    r.raise_for_status()

    reviews = []
    for rv in r.json():
        reviews.append({
            "user": rv.get("user", {}).get("login", "unknown"),
            "state": rv["state"],  # APPROVED | CHANGES_REQUESTED | COMMENTED
            "submitted_at": rv.get("submitted_at"),
        })
    return reviews


# ══════════════════════════════════════════════════════════════════
# GitHub Actions / CI-CD Methods
# ══════════════════════════════════════════════════════════════════

# ── Workflow Runs (CI pipelines) ─────────────────────────────────
async def get_workflow_runs(
    token: str,
    owner: str,
    repo: str,
    branch: Optional[str] = None,
    actor: Optional[str] = None,
    status: Optional[str] = None,
    per_page: int = 30,
) -> dict[str, Any]:
    """List GitHub Actions workflow runs, optionally filtered by branch/actor/status."""
    params: dict[str, str] = {"per_page": str(per_page)}
    if branch:
        params["branch"] = branch
    if actor:
        params["actor"] = actor
    if status:
        params["status"] = status  # completed, success, failure, etc.

    url = f"{GITHUB_API}/repos/{owner}/{repo}/actions/runs"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token), params=params)
    if r.status_code == 404:
        return {"total_count": 0, "runs": []}
    r.raise_for_status()
    data = r.json()

    runs = []
    for run in data.get("workflow_runs", []):
        runs.append({
            "run_id": run["id"],
            "name": run.get("name", ""),
            "status": run["status"],            # queued | in_progress | completed
            "conclusion": run.get("conclusion"),  # success | failure | cancelled | ...
            "branch": run.get("head_branch", ""),
            "event": run.get("event", ""),        # push | pull_request | schedule
            "created_at": run.get("created_at"),
            "updated_at": run.get("updated_at"),
            "run_attempt": run.get("run_attempt", 1),
            "actor": run.get("actor", {}).get("login", ""),
        })
    return {"total_count": data.get("total_count", 0), "runs": runs}


# ── Workflow Run Jobs (detailed steps) ──────────────────────────
async def get_workflow_run_jobs(
    token: str, owner: str, repo: str, run_id: int
) -> list[dict[str, Any]]:
    """Return jobs for a specific workflow run (build steps, test steps, deploy steps)."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token))
    if r.status_code == 404:
        return []
    r.raise_for_status()

    jobs = []
    for job in r.json().get("jobs", []):
        steps = []
        for s in job.get("steps", []):
            steps.append({
                "name": s["name"],
                "status": s["status"],
                "conclusion": s.get("conclusion"),
                "number": s["number"],
            })
        jobs.append({
            "job_id": job["id"],
            "name": job["name"],
            "status": job["status"],
            "conclusion": job.get("conclusion"),
            "started_at": job.get("started_at"),
            "completed_at": job.get("completed_at"),
            "steps": steps,
        })
    return jobs


# ── GitHub Deployments ───────────────────────────────────────────
async def get_deployments(
    token: str,
    owner: str,
    repo: str,
    environment: Optional[str] = None,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """Return GitHub Deployments with their latest status."""
    params: dict[str, str] = {"per_page": str(per_page)}
    if environment:
        params["environment"] = environment

    url = f"{GITHUB_API}/repos/{owner}/{repo}/deployments"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token), params=params)
    if r.status_code == 404:
        return []
    r.raise_for_status()

    deployments = []
    for dep in r.json():
        # Get latest status for each deployment
        status_url = dep.get("statuses_url", "")
        dep_status = "unknown"
        if status_url:
            async with httpx.AsyncClient(timeout=10) as client2:
                sr = await client2.get(status_url, headers=_headers(token))
            if sr.status_code == 200:
                statuses = sr.json()
                if statuses:
                    dep_status = statuses[0].get("state", "unknown")

        deployments.append({
            "deployment_id": dep["id"],
            "environment": dep.get("environment", ""),
            "ref": dep.get("ref", ""),
            "sha": dep.get("sha", ""),
            "creator": dep.get("creator", {}).get("login", ""),
            "created_at": dep.get("created_at"),
            "status": dep_status,
            "description": dep.get("description", ""),
        })
    return deployments


# ══════════════════════════════════════════════════════════════════
# GitHub Check Runs / QA & Test Results
# ══════════════════════════════════════════════════════════════════

# ── Check Runs (test results per commit) ─────────────────────────
async def get_check_runs(
    token: str,
    owner: str,
    repo: str,
    ref: str,
    per_page: int = 30,
) -> dict[str, Any]:
    """Get check runs for a git reference (branch, tag, or SHA).
    Returns test suite results reported by CI."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{ref}/check-runs"
    params = {"per_page": str(per_page)}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token), params=params)
    if r.status_code == 404:
        return {"total_count": 0, "check_runs": []}
    r.raise_for_status()
    data = r.json()

    runs = []
    for cr in data.get("check_runs", []):
        output = cr.get("output", {})
        runs.append({
            "check_run_id": cr["id"],
            "name": cr["name"],
            "status": cr["status"],           # queued | in_progress | completed
            "conclusion": cr.get("conclusion"),  # success | failure | neutral | ...
            "started_at": cr.get("started_at"),
            "completed_at": cr.get("completed_at"),
            "output_title": output.get("title", ""),
            "output_summary": output.get("summary", ""),
            "annotations_count": output.get("annotations_count", 0),
        })
    return {"total_count": data.get("total_count", 0), "check_runs": runs}


# ── Check Run Annotations (test failures / warnings) ────────────
async def get_check_run_annotations(
    token: str, owner: str, repo: str, check_run_id: int
) -> list[dict[str, Any]]:
    """Get annotations (failure details, warnings) for a specific check run."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/check-runs/{check_run_id}/annotations"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=_headers(token))
    if r.status_code == 404:
        return []
    r.raise_for_status()

    annotations = []
    for ann in r.json():
        annotations.append({
            "path": ann.get("path", ""),
            "start_line": ann.get("start_line"),
            "end_line": ann.get("end_line"),
            "annotation_level": ann.get("annotation_level", ""),  # warning | failure | notice
            "message": ann.get("message", ""),
            "title": ann.get("title", ""),
        })
    return annotations


