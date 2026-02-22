"""
Agent 1 — Enterprise GitHub Developer Verification (Chain-of-Thought)

Verifies developer progress by querying real GitHub API data:
  Branch → Commits → PR → Reviews → Files Changed

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
WEIGHTS = {
    "branch_created": 10,
    "commits_pushed": 20,
    "pr_created": 20,
    "pr_reviewed": 15,
    "pr_merged": 20,
    "file_alignment": 15,
}

# ── Chain-of-Thought LLM Prompt ─────────────────────────────────
COT_SYSTEM_PROMPT = """You are an expert GitHub Code Analysis AI agent for ExecSense.
You are given REAL data fetched from the GitHub API about a developer's progress.

**You MUST think step-by-step before answering.**

## Chain-of-Thought Steps
1. COMMIT ANALYSIS — Count commits, review commit messages for quality and consistency.
   Note frequency patterns, co-authored commits, and message conventions.
2. CODE QUALITY ASSESSMENT — Examine file changes: Are they in the expected module?
   Check for large diffs, binary files, or unusual patterns indicating code smells.
3. FILE ALIGNMENT CHECK — What fraction of changed files belong to the expected module?
   Flag any out-of-scope file modifications. Assess scope drift risk.
4. PR REVIEW STATUS — Has a PR been created? Is it reviewed/approved/merged?
   Check review comments for quality feedback. Note unresolved conversations.
5. RISK SYNTHESIS — Based on steps 1-4, assess overall risk level (LOW/MEDIUM/HIGH).
   Produce actionable recommendations for the developer.

## Output Format
Return ONLY valid JSON (no markdown fences) in this exact shape:
{
  "chain_of_thought": "<your step-by-step reasoning as a single string>",
  "summary": "<2-3 sentence contribution summary>",
  "code_quality_notes": "<assessment of code quality>",
  "risk_level": "LOW|MEDIUM|HIGH",
  "recommendations": ["<suggestion 1>", "<suggestion 2>", ...],
  "quality_score": <0-100 integer>,
  "issues": ["<issue 1>", ...],
  "suggestions": ["<improvement 1>", ...],
  "security_issues": []
}

Be specific — reference actual branch names, commit messages, and file names from the data.
"""

analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", COT_SYSTEM_PROMPT),
    ("human", (
        "Task Description: {task_description}\n"
        "Expected Branch: {expected_branch}\n"
        "Expected Module: {expected_module}\n\n"
        "=== GitHub Data ===\n{github_data}"
    )),
])


# ── File alignment score ────────────────────────────────────────
def _compute_file_alignment(files: list[dict], expected_module: str) -> float:
    """Score 0.0–1.0: fraction of changed files in the expected module."""
    if not files or not expected_module:
        return 0.0
    module = expected_module.strip("/").lower()
    matching = sum(
        1 for f in files if f["filename"].lower().startswith(module)
    )
    return round(matching / len(files), 2) if files else 0.0


# ── Progress score calculator ───────────────────────────────────
def _compute_progress_score(signals: dict[str, Any]) -> int:
    """Compute weighted progress score (0–100)."""
    score = 0

    # Branch created (10 pts)
    if signals.get("branch_exists"):
        score += WEIGHTS["branch_created"]

    # Commits pushed (up to 20 pts — 4 pts per commit, max 5)
    commit_count = signals.get("commit_count", 0)
    score += min(commit_count * 4, WEIGHTS["commits_pushed"])

    # PR created (20 pts)
    if signals.get("pr_created"):
        score += WEIGHTS["pr_created"]

    # PR reviewed/approved (15 pts)
    if signals.get("pr_approved"):
        score += WEIGHTS["pr_reviewed"]
    elif signals.get("pr_review_count", 0) > 0:
        score += WEIGHTS["pr_reviewed"] // 2  # partial credit

    # PR merged (20 pts)
    if signals.get("pr_merged"):
        score += WEIGHTS["pr_merged"]

    # File alignment (up to 15 pts)
    alignment = signals.get("file_alignment", 0.0)
    score += int(alignment * WEIGHTS["file_alignment"])

    return min(score, 100)


# ── Rule-based CoT fallback ─────────────────────────────────────
def _rule_based_code_analysis(
    signals: dict[str, Any],
    commits: list[dict],
    prs: list[dict],
    all_files: list[dict],
    all_reviews: list[dict],
    expected_branch: str,
    expected_module: str,
    progress_score: int,
) -> dict:
    """Deterministic heuristic analysis when no LLM is available."""

    branch_exists = signals.get("branch_exists", False)
    commit_count = signals.get("commit_count", 0)
    pr_created = signals.get("pr_created", False)
    pr_merged = signals.get("pr_merged", False)
    pr_approved = signals.get("pr_approved", False)
    pr_review_count = signals.get("pr_review_count", 0)
    file_alignment = signals.get("file_alignment", 0.0)

    # ── Chain of thought trace ──
    cot = (
        f"Step 1 — COMMIT ANALYSIS: "
        f"{'Branch exists' if branch_exists else 'Branch NOT found'} "
        f"('{expected_branch}'). "
        f"{commit_count} commit(s) found. "
    )
    if commits:
        msgs = [c.get("message", "")[:50] for c in commits[:3]]
        cot += f"Latest messages: {'; '.join(msgs)}. "
    else:
        cot += "No commits to analyse. "

    cot += (
        f"\nStep 2 — CODE QUALITY: "
        f"{len(all_files)} files changed. "
    )
    if all_files:
        exts = set(f.get("filename", "").rsplit(".", 1)[-1] for f in all_files if "." in f.get("filename", ""))
        cot += f"File types: {', '.join(sorted(exts))}. "
        large_diffs = [f for f in all_files if f.get("changes", 0) > 300]
        if large_diffs:
            cot += f"{len(large_diffs)} large diff(s) detected (>300 lines). "
    else:
        cot += "No file changes to assess. "

    cot += (
        f"\nStep 3 — FILE ALIGNMENT: "
        f"{round(file_alignment * 100, 1)}% of changed files are in the expected module "
        f"('{expected_module}'). "
    )
    if file_alignment < 0.5:
        cot += "⚠ Significant scope drift — many files outside expected module. "
    elif file_alignment < 0.8:
        cot += "Moderate alignment — some out-of-scope changes. "
    else:
        cot += "Good alignment — changes focused on expected module. "

    cot += (
        f"\nStep 4 — PR REVIEW STATUS: "
        f"{'PR created' if pr_created else 'No PR created'}. "
    )
    if pr_created:
        cot += (
            f"{'Merged ✓' if pr_merged else 'Not merged'}. "
            f"{'Approved ✓' if pr_approved else 'Not approved'}. "
            f"{pr_review_count} review(s). "
        )

    # Risk assessment
    risk = "LOW"
    issues = []
    if not branch_exists:
        risk = "HIGH"
        issues.append("Expected branch does not exist")
    if commit_count == 0:
        risk = "HIGH"
        issues.append("No commits found from the developer")
    if file_alignment < 0.5:
        risk = max(risk, "MEDIUM")
        issues.append(f"File alignment at {round(file_alignment * 100)}% — possible scope drift")
    if not pr_created and commit_count > 3:
        risk = max(risk, "MEDIUM")
        issues.append("Multiple commits but no PR created — review cycle not started")

    cot += (
        f"\nStep 5 — RISK SYNTHESIS: Overall risk = {risk}. "
        f"Progress score = {progress_score}/100. "
        f"{len(issues)} issue(s) identified. "
        f"Recommendations generated based on analysis."
    )

    # Recommendations
    recommendations = []
    if not pr_created:
        recommendations.append("Create a pull request to start the code review cycle")
    if file_alignment < 0.7:
        recommendations.append(f"Focus changes on the '{expected_module}' module — avoid touching unrelated files")
    if not pr_approved and pr_created:
        recommendations.append("Request a peer review to move toward approval")
    if commit_count < 3:
        recommendations.append("Increase commit frequency — aim for small, focused commits")
    if not recommendations:
        recommendations.append("Continue the current work pattern — good progress")

    # Summary
    summary = (
        f"Developer has {commit_count} commit(s) on branch '{expected_branch}'. "
        f"{'PR created and ' + ('merged' if pr_merged else 'open') if pr_created else 'No PR yet'}. "
        f"File alignment at {round(file_alignment * 100)}%. Progress score: {progress_score}/100."
    )

    return {
        "chain_of_thought": cot,
        "summary": summary,
        "code_quality_notes": f"{len(all_files)} files changed across {len(set(f.get('filename', '').rsplit('/', 1)[0] for f in all_files))} directories.",
        "risk_level": risk,
        "recommendations": recommendations,
        "quality_score": progress_score,
        "issues": issues,
        "suggestions": recommendations,
        "security_issues": [],
    }


# ── Main verification function ──────────────────────────────────
async def verify_developer_progress(
    github_token: str,
    owner: str,
    repo: str,
    expected_branch: str,
    expected_module: str,
    github_username: str,
    task_description: str,
) -> dict[str, Any]:
    """
    Full enterprise verification flow with Chain-of-Thought:
    1. Check branch existence
    2. Fetch commits by author on branch
    3. Fetch PRs matching the branch
    4. For each PR: fetch files changed and reviews
    5. Compute progress score
    6. Run CoT analysis (LLM or rule-based fallback)
    """

    # 1 — Branch
    branch_info = await github_service.check_branch(
        github_token, owner, repo, expected_branch
    )
    branch_exists = branch_info["exists"]

    # 2 — Commits
    commits = []
    if branch_exists:
        commits = await github_service.get_commits(
            github_token, owner, repo, expected_branch, github_username
        )

    # 3 — Pull Requests
    prs = await github_service.get_pull_requests(
        github_token, owner, repo, expected_branch
    )

    # 4 — PR details (files + reviews) for the first matching PR
    all_files: list[dict] = []
    all_reviews: list[dict] = []
    pr_created = len(prs) > 0
    pr_merged = False
    pr_approved = False
    pr_review_count = 0

    if prs:
        main_pr = prs[0]  # most relevant PR
        pr_merged = main_pr.get("merged_at") is not None

        all_files = await github_service.get_pr_files(
            github_token, owner, repo, main_pr["pr_number"]
        )
        all_reviews = await github_service.get_pr_reviews(
            github_token, owner, repo, main_pr["pr_number"]
        )
        pr_review_count = len(all_reviews)
        pr_approved = any(r["state"] == "APPROVED" for r in all_reviews)

    # 5 — Compute scores
    file_alignment = _compute_file_alignment(all_files, expected_module)

    signals = {
        "branch_exists": branch_exists,
        "commit_count": len(commits),
        "pr_created": pr_created,
        "pr_merged": pr_merged,
        "pr_approved": pr_approved,
        "pr_review_count": pr_review_count,
        "file_alignment": file_alignment,
    }

    progress_score = _compute_progress_score(signals)

    # 6 — CoT analysis: LLM first, fallback to rule-based
    github_data_summary = json.dumps({
        "branch": branch_info,
        "commits": commits[:10],
        "pull_requests": prs,
        "files_changed": all_files[:20],
        "reviews": all_reviews,
    }, indent=2, default=str)

    try:
        chain = analysis_prompt | get_llm()
        llm_response = await chain.ainvoke({
            "task_description": task_description,
            "expected_branch": expected_branch,
            "expected_module": expected_module,
            "github_data": github_data_summary,
        })
        raw = llm_response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
        llm_insights = json.loads(raw)
        llm_insights["source"] = "ai"
    except Exception as e:
        print(f"⚠️  LLM unavailable for code analysis ({e}), using rule-based CoT")
        llm_insights = _rule_based_code_analysis(
            signals, commits, prs, all_files, all_reviews,
            expected_branch, expected_module, progress_score,
        )
        llm_insights["source"] = "rule_based"

    # ── Build response ──
    chain_of_thought = llm_insights.get("chain_of_thought", "")
    code_quality_score = llm_insights.get("quality_score", progress_score)
    ai_comment = llm_insights.get("summary", "Code analysis complete.")
    security_issues = llm_insights.get("security_issues", [])
    suggestions = llm_insights.get("suggestions", [])

    return {
        "progress_score": progress_score,
        "alignment_score": round(file_alignment * 100, 1),
        "signals": signals,
        "branch": branch_info,
        "commits_count": len(commits),
        "commits_latest": commits[:5],
        "pull_requests": prs,
        "files_changed_count": len(all_files),
        "files_changed": all_files[:20],
        "reviews": all_reviews,
        "llm_insights": llm_insights,
        "weights": WEIGHTS,
        "chain_of_thought": chain_of_thought,
        "source": llm_insights.get("source", "unknown"),
        # ── Fields for DevAIFeedback.jsx & PMReviewQueue.jsx ──
        "code_quality": {
            "score": code_quality_score,
            "issues": llm_insights.get("issues", []),
            "suggestions": suggestions,
        },
        "security": {"vulnerabilities": security_issues},
        "ai_comment": ai_comment if len(ai_comment) < 150 else ai_comment[:147] + "...",
    }


# ── Legacy wrapper for backward-compat with supervisor ───────────
async def analyze_code(task_description: str, code_data: str) -> str:
    """Backward-compatible: runs LLM-only analysis when called via
    the old `github_code_analysis` task type."""
    try:
        chain = analysis_prompt | get_llm()
        response = await chain.ainvoke({
            "task_description": task_description,
            "expected_branch": "N/A",
            "expected_module": "N/A",
            "github_data": code_data,
        })
        return response.content
    except Exception:
        # Rule-based fallback for legacy path
        return json.dumps({
            "chain_of_thought": "Legacy analysis: LLM unavailable, returning basic assessment.",
            "summary": "Code analysis completed via rule-based engine.",
            "code_quality_notes": "Unable to assess without LLM.",
            "risk_level": "UNKNOWN",
            "recommendations": ["Configure GOOGLE_API_KEY for full AI analysis"],
            "quality_score": 50,
        })
