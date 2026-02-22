"""
Agent 4 — Enterprise QA Test Verifier (Chain-of-Thought)

Verifies QA progress by querying:
  - GitHub Check Runs (test suite results from CI)
  - GitHub Actions workflow runs (regression CI)
  - Internal task/bug data from MongoDB
  - File coverage from PR changed files

Uses Chain-of-Thought (CoT) reasoning to produce a visible reasoning
trace, then a structured assessment.  Falls back to a rule-based
heuristic engine when no LLM is available.

Output includes:
  chain_of_thought: str   — visible step-by-step reasoning
"""

from __future__ import annotations

import json
from typing import Any, Optional

from langchain_core.prompts import ChatPromptTemplate

from app.ai_agents.llm_provider import get_llm
from app.ai_agents import github_service
from app.database import tasks_collection

# ── Scoring weights ──────────────────────────────────────────────
QA_WEIGHTS = {
    "coverage": 30,
    "test_execution": 25,
    "fail_rate": 20,
    "bug_closure": 15,
    "regression_pass": 10,
}

# Coverage threshold (minimum acceptable %)
COVERAGE_THRESHOLD = 60.0

# Test-related check run name patterns
TEST_PATTERNS = (
    "test", "jest", "pytest", "mocha", "junit", "rspec",
    "cypress", "playwright", "coverage", "lint", "check",
    "ci", "build", "unit", "integration", "e2e",
)

# ── Chain-of-Thought LLM Prompt ─────────────────────────────────
COT_SYSTEM_PROMPT = """You are an expert QA & Test Verification AI agent for ExecSense.
You are given REAL data fetched from GitHub (check runs, test results,
annotations, coverage info) and internal bug/task data.

**You MUST think step-by-step before answering.**

## Chain-of-Thought Steps
1. TEST RESULTS — Count total check runs, passed, failed, and skipped.
   Identify which test suites failed and their specific error messages.
   Note test execution completeness.
2. COVERAGE ANALYSIS — Extract coverage percentage from check run outputs.
   Compare against the threshold (60%). Identify under-tested modules
   or files with zero coverage.
3. BUG ASSESSMENT — Review open vs closed bugs. Calculate bug closure rate.
   Identify any critical bugs that remain open. Assess bug backlog health.
4. REGRESSION CHECK — Compare latest CI run against previous runs.
   Detect if any previously passing tests are now failing. Identify
   the specific tests and files involved in regression.
5. QUALITY SYNTHESIS — Based on steps 1-4, compute overall quality score.
   Determine rejection risk. Generate specific, actionable recommendations.

## Output Format
Return ONLY valid JSON (no markdown fences) in this exact shape:
{
  "chain_of_thought": "<your step-by-step reasoning as a single string>",
  "test_summary": "<total suites, passed, failed summary>",
  "coverage_assessment": "LOW|MEDIUM|HIGH",
  "critical_failures": ["<failure 1>", "<failure 2>", ...],
  "regression_status": "YES|NO — <details>",
  "rejection_risk": <0-100>,
  "quality_score": <0-100>,
  "recommendations": ["<fix 1>", "<fix 2>", ...]
}

Be specific — reference actual check names, file paths, and bug IDs from the data.
"""

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", COT_SYSTEM_PROMPT),
    ("human", (
        "Project: {project_name}\n"
        "Task: {task_description}\n"
        "Branch: {branch}\n\n"
        "=== QA Data ===\n{qa_data}"
    )),
])


# ── Parse check run outputs for coverage numbers ────────────────
def _extract_coverage(check_runs: list[dict]) -> Optional[float]:
    """Try to extract coverage percentage from check run output summaries."""
    import re
    for cr in check_runs:
        summary = (cr.get("output_summary") or "").lower()
        title = (cr.get("output_title") or "").lower()
        text = summary + " " + title
        match = re.search(r"(\d+\.?\d*)\s*%\s*(?:coverage|cov|covered)", text)
        if match:
            return float(match.group(1))
        match = re.search(r"(?:coverage|cov|covered)[:\s]+(\d+\.?\d*)\s*%", text)
        if match:
            return float(match.group(1))
    return None


# ── QA Score Computation ─────────────────────────────────────────
def _compute_qa_score(signals: dict[str, Any]) -> int:
    """Compute weighted QA progress score (0–100)."""
    score = 0

    # Coverage (30 pts)
    coverage = signals.get("coverage_pct")
    if coverage is not None:
        if coverage >= 80:
            score += QA_WEIGHTS["coverage"]
        elif coverage >= COVERAGE_THRESHOLD:
            score += int((coverage / 80) * QA_WEIGHTS["coverage"])
        else:
            score += int((coverage / 80) * QA_WEIGHTS["coverage"] * 0.5)

    # Test execution (25 pts)
    total_checks = signals.get("total_check_runs", 0)
    completed = signals.get("completed_checks", 0)
    if total_checks > 0 and completed > 0:
        score += QA_WEIGHTS["test_execution"]
    elif total_checks > 0:
        score += QA_WEIGHTS["test_execution"] // 2

    # Fail rate (20 pts — lower is better)
    total_checks_for_fail = signals.get("total_check_runs", 0)
    failed = signals.get("failed_checks", 0)
    if total_checks_for_fail > 0:
        fail_rate = failed / total_checks_for_fail
        if fail_rate == 0:
            score += QA_WEIGHTS["fail_rate"]
        elif fail_rate < 0.1:
            score += int(QA_WEIGHTS["fail_rate"] * 0.7)
        elif fail_rate < 0.3:
            score += int(QA_WEIGHTS["fail_rate"] * 0.3)

    # Bug closure (15 pts)
    open_bugs = signals.get("open_bugs", 0)
    closed_bugs = signals.get("closed_bugs", 0)
    total_bugs = open_bugs + closed_bugs
    if total_bugs > 0:
        closure_rate = closed_bugs / total_bugs
        score += int(closure_rate * QA_WEIGHTS["bug_closure"])
    else:
        score += QA_WEIGHTS["bug_closure"]

    # Regression pass (10 pts)
    has_regression = signals.get("has_regression_failure", False)
    if not has_regression:
        score += QA_WEIGHTS["regression_pass"]

    return min(score, 100)


# ── Rule-based CoT fallback ─────────────────────────────────────
def _rule_based_qa_analysis(
    signals: dict[str, Any],
    failure_details: list[dict],
    qa_score: int,
    branch: str,
) -> dict:
    """Deterministic heuristic analysis when no LLM is available."""

    total_checks = signals.get("total_check_runs", 0)
    passed = signals.get("passed_checks", 0)
    failed = signals.get("failed_checks", 0)
    coverage = signals.get("coverage_pct")
    open_bugs = signals.get("open_bugs", 0)
    closed_bugs = signals.get("closed_bugs", 0)
    has_regression = signals.get("has_regression_failure", False)

    pass_rate = round(passed / total_checks * 100, 1) if total_checks > 0 else 0
    total_bugs = open_bugs + closed_bugs
    closure_rate = round(closed_bugs / total_bugs * 100, 1) if total_bugs > 0 else 100

    # ── Chain of thought trace ──
    cot = (
        f"Step 1 — TEST RESULTS: "
        f"{total_checks} check run(s) on branch '{branch}'. "
        f"{passed} passed, {failed} failed "
        f"(pass rate: {pass_rate}%). "
    )
    if failure_details:
        fail_files = list(set(d.get("file", "?") for d in failure_details[:5]))
        cot += f"Failed in: {', '.join(fail_files)}. "
    elif failed > 0:
        cot += "Failure details not available. "
    else:
        cot += "All tests passing ✓. "

    cot += f"\nStep 2 — COVERAGE ANALYSIS: "
    if coverage is not None:
        cot += (
            f"Coverage at {coverage}%. "
            f"{'Meets' if coverage >= COVERAGE_THRESHOLD else 'Below'} "
            f"the {COVERAGE_THRESHOLD}% threshold. "
        )
        if coverage >= 80:
            cot += "Excellent coverage ✓. "
        elif coverage >= COVERAGE_THRESHOLD:
            cot += "Acceptable coverage but has room for improvement. "
        else:
            cot += "⚠ Coverage needs significant improvement. "
    else:
        cot += "Coverage data not available from check runs. "

    cot += (
        f"\nStep 3 — BUG ASSESSMENT: "
        f"{open_bugs} open bug(s), {closed_bugs} closed bug(s). "
        f"Bug closure rate: {closure_rate}%. "
    )
    if open_bugs > 5:
        cot += "⚠ High bug backlog — quality risk. "
    elif open_bugs > 0:
        cot += "Bug count within acceptable range. "
    else:
        cot += "No open bugs ✓. "

    cot += (
        f"\nStep 4 — REGRESSION CHECK: "
        f"{'⚠ REGRESSION DETECTED — previously passing tests now failing' if has_regression else 'No regression detected ✓'}. "
    )

    # Quality and risk
    rejection_risk = 100 - qa_score
    quality_assessment = "HIGH" if coverage and coverage >= 80 else "MEDIUM" if coverage and coverage >= COVERAGE_THRESHOLD else "LOW"

    critical_failures = []
    for d in failure_details[:5]:
        critical_failures.append(f"{d.get('check', '?')}: {d.get('message', 'failed')[:80]}")

    recommendations = []
    if failed > 0:
        recommendations.append("Fix failing test suites before merging to main branch")
    if coverage is not None and coverage < COVERAGE_THRESHOLD:
        recommendations.append(f"Increase test coverage from {coverage}% to at least {COVERAGE_THRESHOLD}%")
    if open_bugs > 3:
        recommendations.append(f"Prioritize closing {open_bugs} open bugs — focus on critical severity first")
    if has_regression:
        recommendations.append("Investigate regression — compare recent commits to identify breaking change")
    if not recommendations:
        recommendations.append("QA metrics are healthy — continue current testing practices")

    cot += (
        f"\nStep 5 — QUALITY SYNTHESIS: "
        f"QA score = {qa_score}/100. "
        f"Coverage assessment = {quality_assessment}. "
        f"Rejection risk = {rejection_risk}%. "
        f"{len(critical_failures)} critical failure(s). "
        f"{len(recommendations)} recommendation(s) generated."
    )

    return {
        "chain_of_thought": cot,
        "test_summary": f"{total_checks} checks ({pass_rate}% pass rate), {failed} failed",
        "coverage_assessment": quality_assessment,
        "critical_failures": critical_failures,
        "regression_status": f"{'YES — previously passing tests now failing' if has_regression else 'NO — no regressions detected'}",
        "rejection_risk": rejection_risk,
        "quality_score": qa_score,
        "recommendations": recommendations,
    }


# ── Main QA Verification ────────────────────────────────────────
async def verify_qa_progress(
    github_token: str,
    owner: str,
    repo: str,
    branch: str,
    task_description: str,
    project_name: str = "",
    project_id: str = "",
    company_id: str = "",
) -> dict[str, Any]:
    """
    Full enterprise QA verification flow with Chain-of-Thought:
    1. Fetch GitHub Check Runs (test results from CI)
    2. Get annotations for failed checks (failure details)
    3. Fetch CI workflow runs to detect regression
    4. Query internal bug/task data from MongoDB
    5. Extract coverage from check run outputs
    6. Compute QA score
    7. Run CoT analysis (LLM or rule-based fallback)
    """

    # 1 — Check Runs
    checks_data = await github_service.get_check_runs(
        github_token, owner, repo, ref=branch
    )
    all_checks = checks_data.get("check_runs", [])
    total_checks = len(all_checks)
    completed_checks = sum(1 for c in all_checks if c.get("status") == "completed")
    passed_checks = sum(1 for c in all_checks if c.get("conclusion") == "success")
    failed_checks = sum(1 for c in all_checks if c.get("conclusion") == "failure")

    # 2 — Annotations for failed checks
    all_annotations = []
    failure_details = []
    for cr in all_checks:
        if cr.get("conclusion") == "failure" and cr.get("annotations_count", 0) > 0:
            try:
                anns = await github_service.get_check_run_annotations(
                    github_token, owner, repo, cr["check_run_id"]
                )
                all_annotations.extend(anns)
                for ann in anns:
                    if ann.get("annotation_level") in ("failure", "warning"):
                        failure_details.append({
                            "check": cr["name"],
                            "file": ann.get("path", ""),
                            "line": ann.get("start_line"),
                            "message": ann.get("message", ""),
                            "level": ann.get("annotation_level"),
                        })
            except Exception:
                pass

    # 3 — Regression detection
    has_regression = False
    try:
        runs_data = await github_service.get_workflow_runs(
            github_token, owner, repo, branch=branch, per_page=10
        )
        runs = runs_data.get("runs", [])
        if len(runs) >= 2:
            latest = runs[0].get("conclusion")
            previous = runs[1].get("conclusion")
            if latest == "failure" and previous == "success":
                has_regression = True
    except Exception:
        pass

    # 4 — Internal bug/task data
    open_bugs = 0
    closed_bugs = 0
    if project_id and company_id:
        try:
            open_bugs = await tasks_collection.count_documents({
                "project_id": project_id,
                "company_id": company_id,
                "status": {"$in": ["open", "in_progress", "reopened"]},
                "$or": [
                    {"title": {"$regex": "bug", "$options": "i"}},
                    {"description": {"$regex": "bug", "$options": "i"}},
                ],
            })
            closed_bugs = await tasks_collection.count_documents({
                "project_id": project_id,
                "company_id": company_id,
                "status": {"$in": ["closed", "completed", "resolved"]},
                "$or": [
                    {"title": {"$regex": "bug", "$options": "i"}},
                    {"description": {"$regex": "bug", "$options": "i"}},
                ],
            })
        except Exception:
            pass

    # 5 — Coverage
    coverage_pct = _extract_coverage(all_checks)

    # 6 — Compute QA score
    signals = {
        "total_check_runs": total_checks,
        "completed_checks": completed_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "coverage_pct": coverage_pct,
        "open_bugs": open_bugs,
        "closed_bugs": closed_bugs,
        "has_regression_failure": has_regression,
        "annotation_count": len(all_annotations),
    }
    qa_score = _compute_qa_score(signals)

    # 7 — CoT analysis: LLM first, fallback to rule-based
    qa_data_summary = json.dumps({
        "check_runs": all_checks[:15],
        "failure_details": failure_details[:20],
        "coverage_pct": coverage_pct,
        "open_bugs": open_bugs,
        "closed_bugs": closed_bugs,
        "has_regression": has_regression,
    }, indent=2, default=str)

    try:
        chain = analysis_prompt | get_llm()
        llm_response = await chain.ainvoke({
            "project_name": project_name,
            "task_description": task_description,
            "branch": branch,
            "qa_data": qa_data_summary,
        })
        raw = llm_response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
        llm_insights = json.loads(raw)
        llm_insights["source"] = "ai"
    except Exception as e:
        print(f"⚠️  LLM unavailable for QA analysis ({e}), using rule-based CoT")
        llm_insights = _rule_based_qa_analysis(
            signals, failure_details, qa_score, branch,
        )
        llm_insights["source"] = "rule_based"

    # ── Build response ──
    chain_of_thought = llm_insights.get("chain_of_thought", "")

    ai_highlights = []
    if failed_checks > 0:
        ai_highlights.append({"text": f"{failed_checks} test suite(s) failing in CI. Investigate before merge.", "type": "danger"})
    if open_bugs > 3:
        ai_highlights.append({"text": f"{open_bugs} open bugs remain — {open_bugs - 3} above threshold.", "type": "warning"})
    elif open_bugs > 0:
        ai_highlights.append({"text": f"{open_bugs} open bugs — within acceptable range.", "type": "info"})
    cov = coverage_pct or 0
    if cov >= COVERAGE_THRESHOLD:
        ai_highlights.append({"text": f"Test coverage at {cov}% — meets the {COVERAGE_THRESHOLD}% threshold.", "type": "success"})
    else:
        ai_highlights.append({"text": f"Test coverage at {cov}% — below {COVERAGE_THRESHOLD}% threshold.", "type": "warning"})
    if has_regression:
        ai_highlights.append({"text": "Regression detected — previously passing tests now failing.", "type": "danger"})
    else:
        ai_highlights.append({"text": "No regression detected this sprint.", "type": "success"})

    regression_pass_rate = round(passed_checks / total_checks * 100, 1) if total_checks > 0 else 100.0

    return {
        "qa_score": qa_score,
        "signals": signals,
        "check_runs_summary": {
            "total": total_checks,
            "completed": completed_checks,
            "passed": passed_checks,
            "failed": failed_checks,
        },
        "coverage": {
            "percentage": coverage_pct,
            "meets_threshold": (coverage_pct or 0) >= COVERAGE_THRESHOLD,
            "threshold": COVERAGE_THRESHOLD,
        },
        "failures": {
            "count": len(failure_details),
            "details": failure_details[:10],
        },
        "bugs": {
            "open": open_bugs,
            "closed": closed_bugs,
            "closure_rate": round(closed_bugs / (open_bugs + closed_bugs) * 100, 1) if (open_bugs + closed_bugs) > 0 else 100.0,
        },
        "regression": {
            "detected": has_regression,
        },
        "llm_insights": llm_insights,
        "weights": QA_WEIGHTS,
        "chain_of_thought": chain_of_thought,
        "source": llm_insights.get("source", "unknown"),
        # ── Fields for QADashboard.jsx AI Highlights ──
        "ai_highlights": ai_highlights[:3],
        "regression_pass_rate": regression_pass_rate,
    }


# ── Legacy wrapper for backward-compat with supervisor ───────────
async def verify_tests(project_name: str, task_description: str, test_data: str) -> str:
    """Backward-compatible: runs LLM-only analysis when called via
    the old `qa_test_verifier` task type."""
    try:
        chain = analysis_prompt | get_llm()
        response = await chain.ainvoke({
            "project_name": project_name,
            "task_description": task_description,
            "branch": "N/A",
            "qa_data": test_data,
        })
        return response.content
    except Exception:
        return json.dumps({
            "chain_of_thought": "Legacy analysis: LLM unavailable, returning basic assessment.",
            "test_summary": "QA analysis completed via rule-based engine.",
            "quality_score": 50,
            "recommendations": ["Configure GOOGLE_API_KEY for full AI analysis"],
        })
