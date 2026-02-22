"""
Agent 2 — Enterprise CI/CD & DevOps Verification (Chain-of-Thought)

Verifies DevOps progress by querying real GitHub Actions API data:
  CI triggered? → Build success? → Deploy success? → Healthy?

Uses Chain-of-Thought (CoT) reasoning to produce a visible reasoning
trace, then a structured assessment.  Falls back to a rule-based
heuristic engine when no LLM is available.

Output includes:
  chain_of_thought: str   — visible step-by-step reasoning
"""

from __future__ import annotations

import json
from typing import Any

from langchain_core.prompts import ChatPromptTemplate

from app.ai_agents.llm_provider import get_llm
from app.ai_agents import github_service

# ── Scoring weights ──────────────────────────────────────────────
DEVOPS_WEIGHTS = {
    "ci_success": 30,
    "deployment_success": 30,
    "infra_files_changed": 15,
    "monitoring_healthy": 15,
    "no_rollback": 10,
}

# ── Infra file patterns (Terraform, Docker, K8s, CI configs) ────
INFRA_PATTERNS = (
    "terraform/", ".tf", "Dockerfile", "docker-compose",
    "k8s/", "kubernetes/", ".github/workflows/", "Jenkinsfile",
    "cloudbuild", ".gitlab-ci", "helm/", "ansible/",
    "infra/", "deploy/", "scripts/deploy",
)

# ── Chain-of-Thought LLM Prompt ─────────────────────────────────
COT_SYSTEM_PROMPT = """You are an expert CI/CD & DevOps Analysis AI agent for ExecSense.
You are given REAL data fetched from the GitHub Actions API about a DevOps engineer's
pipeline runs, deployments, and infrastructure changes.

**You MUST think step-by-step before answering.**

## Chain-of-Thought Steps
1. PIPELINE STATUS — Count total workflow runs, success rate, and failure rate.
   Identify which pipelines failed and on which branches. Note patterns in failures.
2. BUILD ANALYSIS — Examine the latest run's jobs. Check for flaky tests, timeout
   issues, or dependency installation failures. Assess build health.
3. DEPLOYMENT HEALTH — Review deployment history. Check if deploys succeeded,
   if any rollbacks occurred, and the deployment frequency. Score reliability.
4. INFRA CHANGES — Check which infrastructure files were modified (Terraform,
   Docker, K8s, CI configs). Assess the risk of infrastructure drift.
5. RELIABILITY SYNTHESIS — Based on steps 1-4, compute overall risk level.
   Determine delivery impact. Generate actionable recommendations.

## Output Format
Return ONLY valid JSON (no markdown fences) in this exact shape:
{
  "chain_of_thought": "<your step-by-step reasoning as a single string>",
  "pipeline_summary": "<CI/CD pipeline status summary>",
  "deployment_health": <0-100 score>,
  "root_cause": "<root cause of any failures, or 'None detected'>",
  "risk_level": "LOW|MEDIUM|HIGH",
  "delivery_impact": "<YES/NO + explanation>",
  "recommendations": ["<fix 1>", "<fix 2>", ...]
}

Be specific — reference actual workflow names, job names, and file paths from the data.
"""

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", COT_SYSTEM_PROMPT),
    ("human", (
        "Task: {task_description}\n"
        "Branch: {branch}\n\n"
        "=== CI/CD Data ===\n{cicd_data}"
    )),
])


# ── Infra file alignment check ──────────────────────────────────
def _check_infra_files(files: list[dict]) -> tuple[int, list[str]]:
    """Count how many changed files are infra-related. Return count and filenames."""
    infra_files = []
    for f in files:
        fname = f.get("filename", "").lower()
        if any(pat.lower() in fname for pat in INFRA_PATTERNS):
            infra_files.append(f["filename"])
    return len(infra_files), infra_files


# ── DevOps Progress Score ────────────────────────────────────────
def _compute_devops_score(signals: dict[str, Any]) -> int:
    """Compute weighted DevOps progress score (0–100)."""
    score = 0

    # CI success (30 pts)
    ci_total = signals.get("ci_total_runs", 0)
    ci_success = signals.get("ci_success_count", 0)
    if ci_total > 0:
        ci_rate = ci_success / ci_total
        score += int(ci_rate * DEVOPS_WEIGHTS["ci_success"])

    # Deployment success (30 pts)
    dep_total = signals.get("deployment_total", 0)
    dep_success = signals.get("deployment_success_count", 0)
    if dep_total > 0:
        dep_rate = dep_success / dep_total
        score += int(dep_rate * DEVOPS_WEIGHTS["deployment_success"])
    elif ci_success > 0:
        score += DEVOPS_WEIGHTS["deployment_success"] // 3

    # Infra files changed (15 pts)
    infra_count = signals.get("infra_files_count", 0)
    if infra_count > 0:
        score += DEVOPS_WEIGHTS["infra_files_changed"]

    # Monitoring healthy (15 pts)
    recent_failures = signals.get("recent_failure_count", 0)
    if recent_failures == 0:
        score += DEVOPS_WEIGHTS["monitoring_healthy"]
    elif recent_failures <= 2:
        score += DEVOPS_WEIGHTS["monitoring_healthy"] // 2

    # No rollback (10 pts)
    has_rollback = signals.get("has_rollback", False)
    if not has_rollback:
        score += DEVOPS_WEIGHTS["no_rollback"]

    return min(score, 100)


# ── Rule-based CoT fallback ─────────────────────────────────────
def _rule_based_devops_analysis(
    signals: dict[str, Any],
    all_runs: list[dict],
    latest_jobs: list[dict],
    deployments: list[dict],
    infra_file_list: list[str],
    branch: str,
    environment: str,
    devops_score: int,
) -> dict:
    """Deterministic heuristic analysis when no LLM is available."""

    ci_total = signals.get("ci_total_runs", 0)
    ci_success = signals.get("ci_success_count", 0)
    ci_failures = signals.get("ci_failure_count", 0)
    dep_total = signals.get("deployment_total", 0)
    dep_success = signals.get("deployment_success_count", 0)
    has_rollback = signals.get("has_rollback", False)
    infra_count = signals.get("infra_files_count", 0)

    ci_rate = round(ci_success / ci_total * 100, 1) if ci_total > 0 else 0

    # ── Chain of thought trace ──
    cot = (
        f"Step 1 — PIPELINE STATUS: "
        f"{ci_total} workflow runs found on branch '{branch}'. "
        f"{ci_success} succeeded, {ci_failures} failed "
        f"(success rate: {ci_rate}%). "
    )
    if ci_failures > 0:
        failed_names = [r.get("name", "?") for r in all_runs if r.get("conclusion") == "failure"][:3]
        cot += f"Failed pipelines: {', '.join(failed_names)}. "
    elif ci_total == 0:
        cot += "No CI runs detected — pipeline may not be configured. "

    cot += f"\nStep 2 — BUILD ANALYSIS: "
    if latest_jobs:
        failed_jobs = [j for j in latest_jobs if j.get("conclusion") == "failure"]
        passed_jobs = [j for j in latest_jobs if j.get("conclusion") == "success"]
        cot += (
            f"{len(latest_jobs)} jobs in latest run. "
            f"{len(passed_jobs)} passed, {len(failed_jobs)} failed. "
        )
        if failed_jobs:
            cot += f"Failed jobs: {', '.join(j.get('name', '?') for j in failed_jobs)}. "
    else:
        cot += "No job data available for latest run. "

    dep_rate = round(dep_success / dep_total * 100, 1) if dep_total > 0 else 0
    cot += (
        f"\nStep 3 — DEPLOYMENT HEALTH: "
        f"{dep_total} deployments to '{environment}'. "
        f"{dep_success} successful ({dep_rate}% success rate). "
        f"{'Rollback detected ⚠' if has_rollback else 'No rollbacks detected ✓'}. "
    )

    cot += (
        f"\nStep 4 — INFRA CHANGES: "
        f"{infra_count} infrastructure file(s) modified. "
    )
    if infra_file_list:
        cot += f"Files: {', '.join(infra_file_list[:5])}. "
    else:
        cot += "No infrastructure-related file changes detected. "

    # Risk assessment
    risk = "LOW"
    root_cause = "None detected"
    recommendations = []

    if ci_failures > ci_success and ci_total > 0:
        risk = "HIGH"
        root_cause = "CI failure rate exceeds success rate — pipeline instability"
        recommendations.append("Investigate and fix failing CI pipelines before merging")
    elif ci_failures > 0:
        risk = "MEDIUM"
        root_cause = f"{ci_failures} pipeline failure(s) detected"
        recommendations.append("Review failed pipeline logs for root cause")

    if has_rollback:
        risk = "HIGH" if risk != "HIGH" else risk
        recommendations.append("Investigate deployment rollback — check for breaking changes")

    if dep_total == 0 and ci_total > 0:
        recommendations.append("Set up automated deployment pipeline for continuous delivery")

    delivery_impact = "NO"
    if risk == "HIGH":
        delivery_impact = f"YES — {root_cause} may delay sprint delivery"
    elif risk == "MEDIUM":
        delivery_impact = f"POSSIBLE — {root_cause} requires monitoring"

    if not recommendations:
        recommendations.append("Pipeline is healthy — maintain current practices")
        recommendations.append("Consider adding deployment monitoring alerts")

    cot += (
        f"\nStep 5 — RELIABILITY SYNTHESIS: Overall risk = {risk}. "
        f"DevOps score = {devops_score}/100. "
        f"Root cause: {root_cause}. "
        f"Delivery impact: {delivery_impact}."
    )

    return {
        "chain_of_thought": cot,
        "pipeline_summary": f"{ci_total} runs ({ci_rate}% pass rate), {dep_total} deployments to {environment}",
        "deployment_health": devops_score,
        "root_cause": root_cause,
        "risk_level": risk,
        "delivery_impact": delivery_impact,
        "recommendations": recommendations,
    }


# ── Main DevOps verification function ───────────────────────────
async def verify_devops_progress(
    github_token: str,
    owner: str,
    repo: str,
    branch: str,
    task_description: str,
    environment: str = "staging",
) -> dict[str, Any]:
    """
    Full enterprise DevOps verification flow with Chain-of-Thought:
    1. Fetch GitHub Actions workflow runs for the branch
    2. Get detailed job info for recent runs
    3. Fetch GitHub Deployments
    4. Check for infra file changes in recent commits
    5. Compute DevOps score
    6. Run CoT analysis (LLM or rule-based fallback)
    """

    # 1 — Workflow runs
    runs_data = await github_service.get_workflow_runs(
        github_token, owner, repo, branch=branch, per_page=20
    )
    all_runs = runs_data.get("runs", [])
    ci_total = len(all_runs)
    ci_success = sum(1 for r in all_runs if r.get("conclusion") == "success")
    ci_failures = sum(1 for r in all_runs if r.get("conclusion") == "failure")

    # 2 — Detailed jobs for the latest run
    latest_jobs = []
    if all_runs:
        latest_run = all_runs[0]
        latest_jobs = await github_service.get_workflow_run_jobs(
            github_token, owner, repo, latest_run["run_id"]
        )

    # 3 — Deployments
    deployments = await github_service.get_deployments(
        github_token, owner, repo, environment=environment
    )
    dep_total = len(deployments)
    dep_success = sum(1 for d in deployments if d.get("status") in ("success", "active"))
    has_rollback = any(
        d.get("status") == "inactive" or "rollback" in (d.get("description") or "").lower()
        for d in deployments
    )

    # 4 — Infra files
    infra_files_count = 0
    infra_file_list: list[str] = []
    try:
        commits = await github_service.get_commits(
            github_token, owner, repo, branch, author="", since=None
        )
        prs = await github_service.get_pull_requests(
            github_token, owner, repo, branch
        )
        if prs:
            pr_files = await github_service.get_pr_files(
                github_token, owner, repo, prs[0]["pr_number"]
            )
            infra_files_count, infra_file_list = _check_infra_files(pr_files)
    except Exception:
        pass

    # 5 — Compute score
    signals = {
        "ci_total_runs": ci_total,
        "ci_success_count": ci_success,
        "ci_failure_count": ci_failures,
        "recent_failure_count": ci_failures,
        "deployment_total": dep_total,
        "deployment_success_count": dep_success,
        "infra_files_count": infra_files_count,
        "has_rollback": has_rollback,
    }
    devops_score = _compute_devops_score(signals)

    # 6 — CoT analysis: LLM first, fallback to rule-based
    cicd_data_summary = json.dumps({
        "workflow_runs": all_runs[:10],
        "latest_run_jobs": latest_jobs[:5],
        "deployments": deployments[:10],
        "infra_files": infra_file_list,
    }, indent=2, default=str)

    try:
        chain = analysis_prompt | get_llm()
        llm_response = await chain.ainvoke({
            "task_description": task_description,
            "branch": branch,
            "cicd_data": cicd_data_summary,
        })
        raw = llm_response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
        llm_insights = json.loads(raw)
        llm_insights["source"] = "ai"
    except Exception as e:
        print(f"⚠️  LLM unavailable for CI/CD analysis ({e}), using rule-based CoT")
        llm_insights = _rule_based_devops_analysis(
            signals, all_runs, latest_jobs, deployments,
            infra_file_list, branch, environment, devops_score,
        )
        llm_insights["source"] = "rule_based"

    # ── Build response ──
    chain_of_thought = llm_insights.get("chain_of_thought", "")

    pipeline_summary = []
    for run in all_runs[:5]:
        pipeline_summary.append({
            "name": run.get("name", run.get("workflow_name", "Pipeline")),
            "status": run.get("conclusion", "running").capitalize() if run.get("conclusion") else "Running",
            "branch": run.get("head_branch", branch),
            "duration": run.get("duration", "—"),
        })

    alert_classification = []
    if ci_failures > 0:
        alert_classification.append({"msg": f"{ci_failures} CI pipeline(s) failed on {branch}", "level": "error", "time": "recent"})
    if has_rollback:
        alert_classification.append({"msg": f"Rollback detected in {environment} deployment", "level": "warning", "time": "recent"})
    if infra_files_count > 0:
        alert_classification.append({"msg": f"{infra_files_count} infrastructure file(s) modified", "level": "info", "time": "recent"})

    deployment_status = {
        "environment": environment,
        "version": deployments[0].get("sha", "")[:8] if deployments else "—",
        "status": "success" if dep_success > 0 else "pending",
    }

    return {
        "devops_score": devops_score,
        "signals": signals,
        "ci_summary": {
            "total_runs": ci_total,
            "successful": ci_success,
            "failed": ci_failures,
            "latest_run": all_runs[0] if all_runs else None,
        },
        "latest_jobs": latest_jobs[:5],
        "deployments": {
            "total": dep_total,
            "successful": dep_success,
            "has_rollback": has_rollback,
            "recent": deployments[:5],
        },
        "infra_changes": {
            "count": infra_files_count,
            "files": infra_file_list,
        },
        "llm_insights": llm_insights,
        "weights": DEVOPS_WEIGHTS,
        "chain_of_thought": chain_of_thought,
        "source": llm_insights.get("source", "unknown"),
        # ── Fields for DevOpsDashboard/Pipelines/Alerts pages ──
        "pipeline_summary": pipeline_summary,
        "alert_classification": alert_classification,
        "deployment_status": deployment_status,
    }


# ── Legacy wrapper for backward-compat with supervisor ───────────
async def analyze_cicd_logs(pipeline_name: str, log_data: str) -> str:
    """Backward-compatible: runs LLM-only analysis when called via
    the old `cicd_log_parsing` task type."""
    try:
        chain = analysis_prompt | get_llm()
        response = await chain.ainvoke({
            "task_description": pipeline_name,
            "branch": "N/A",
            "cicd_data": log_data,
        })
        return response.content
    except Exception:
        return json.dumps({
            "chain_of_thought": "Legacy analysis: LLM unavailable, returning basic assessment.",
            "pipeline_summary": "CI/CD analysis completed via rule-based engine.",
            "risk_level": "UNKNOWN",
            "recommendations": ["Configure GOOGLE_API_KEY for full AI analysis"],
        })
