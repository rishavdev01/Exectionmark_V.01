"""
Sprint Retrospective AI Agent — Chain-of-Thought Analysis

Dedicated agent that analyses all project/task/sprint data from the
database and produces a structured retrospective using chain-of-thought
reasoning.  Falls back to a rule-based heuristic engine when no LLM
is available (missing API key).

Output shape
------------
{
  "went_well":     [str, ...],
  "didnt_go_well": [str, ...],
  "improvements":  [{"action": str, "assignee": str, "deadline": str, "priority": str}, ...],
  "ai_summary":    str,
  "chain_of_thought": str          # visible CoT trace
}
"""

from __future__ import annotations

import json
import traceback
from datetime import datetime, timedelta
from typing import Any

from app.database import (
    tasks_collection,
    stories_collection,
    sprints_collection,
    projects_collection,
    ceo_escalations_collection,
    active_risks_collection,
    performance_members_collection,
)


# ── Data Collection ──────────────────────────────────────────────
async def _collect_sprint_data() -> dict[str, Any]:
    """Gather all relevant collections from MongoDB."""

    tasks = [doc async for doc in tasks_collection.find({}, {"_id": 0})]
    stories = [doc async for doc in stories_collection.find({}, {"_id": 0})]
    sprints = [doc async for doc in sprints_collection.find({}, {"_id": 0})]
    projects = [doc async for doc in projects_collection.find({}, {"_id": 0})]
    escalations = [doc async for doc in ceo_escalations_collection.find({}, {"_id": 0})]
    risks = [doc async for doc in active_risks_collection.find({}, {"_id": 0})]
    members = [doc async for doc in performance_members_collection.find({}, {"_id": 0})]

    return {
        "tasks": tasks,
        "stories": stories,
        "sprints": sprints,
        "projects": projects,
        "escalations": escalations,
        "risks": risks,
        "members": members,
        "collected_at": datetime.utcnow().isoformat(),
    }


# ── Chain-of-Thought Prompt ─────────────────────────────────────
_COT_SYSTEM = """You are the Sprint Retrospective Analyst for Exactiomark.
Your job is to analyse sprint/project data and produce a structured retrospective.

**You MUST think step-by-step before answering.**

## Chain-of-Thought Steps
1. TASK ANALYSIS — Look at task statuses (Done / In Progress / To Do). Calculate completion rate. Identify overdue or delayed tasks.
2. STORY ANALYSIS — Check story statuses, approval states, and risk levels. Note any blocked or high-risk stories.
3. SPRINT HEALTH — Review sprint velocity, burndown, and delivery percentage. Compare planned vs actual.
4. PROJECT STATUS — Evaluate project health, completion percentages, and budget utilisation.
5. ESCALATION & RISK REVIEW — Count active risks and escalations. Identify recurring patterns.
6. TEAM PERFORMANCE — Review individual metrics (alignment, on-time delivery, behaviour scores).
7. SYNTHESIS — Based on steps 1-6, identify what went well, what didn't, and concrete improvement actions.

## Output Format
Return ONLY valid JSON (no markdown fences) in this exact shape:
{
  "chain_of_thought": "<your step-by-step reasoning as a single string>",
  "went_well": ["<observation 1>", "<observation 2>", ...],
  "didnt_go_well": ["<issue 1>", "<issue 2>", ...],
  "improvements": [
    {"action": "<what to do>", "assignee": "<person or role>", "deadline": "<date or timeframe>", "priority": "High|Medium|Low"},
    ...
  ],
  "ai_summary": "<A 3-5 sentence executive summary of the sprint retrospective>"
}

Produce at least 3 items for went_well, 3 for didnt_go_well, and 3 improvement actions.
Be specific — reference actual task IDs, names, and people from the data.
"""


def _build_user_prompt(data: dict) -> str:
    """Build the user prompt with real data from all collections."""
    # Summarise each collection concisely to stay within token limits
    parts = []

    # Tasks summary
    tasks = data.get("tasks", [])
    if tasks:
        done = [t for t in tasks if t.get("status") == "Done"]
        in_prog = [t for t in tasks if t.get("status") == "In Progress"]
        todo = [t for t in tasks if t.get("status") == "To Do"]
        parts.append(f"## Tasks ({len(tasks)} total)\n"
                     f"- Done: {len(done)} | In Progress: {len(in_prog)} | To Do: {len(todo)}\n"
                     f"- Details: {json.dumps(tasks[:15], default=str)}")

    # Stories summary
    stories = data.get("stories", [])
    if stories:
        parts.append(f"## Stories ({len(stories)} total)\n"
                     f"- Details: {json.dumps(stories[:15], default=str)}")

    # Sprints
    sprints = data.get("sprints", [])
    if sprints:
        parts.append(f"## Sprints ({len(sprints)} total)\n"
                     f"- Details: {json.dumps(sprints[:10], default=str)}")

    # Projects
    projects = data.get("projects", [])
    if projects:
        parts.append(f"## Projects ({len(projects)} total)\n"
                     f"- Details: {json.dumps(projects[:10], default=str)}")

    # Escalations
    escalations = data.get("escalations", [])
    if escalations:
        parts.append(f"## Escalations ({len(escalations)} total)\n"
                     f"- Details: {json.dumps(escalations[:10], default=str)}")

    # Risks
    risks = data.get("risks", [])
    if risks:
        parts.append(f"## Active Risks ({len(risks)} total)\n"
                     f"- Details: {json.dumps(risks[:10], default=str)}")

    # Team members
    members = data.get("members", [])
    if members:
        parts.append(f"## Team Performance ({len(members)} members)\n"
                     f"- Details: {json.dumps(members[:10], default=str)}")

    return ("Analyse the following sprint data and produce the retrospective.\n\n"
            + "\n\n".join(parts))


# ── LLM-based analysis ──────────────────────────────────────────
async def _run_llm_analysis(data: dict) -> dict:
    """Use Gemini / HuggingFace with chain-of-thought prompting."""
    from ai_agents.llm_provider import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    llm = get_llm()
    messages = [
        SystemMessage(content=_COT_SYSTEM),
        HumanMessage(content=_build_user_prompt(data)),
    ]

    response = await llm.ainvoke(messages)
    raw = response.content.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

    return json.loads(raw)


# ── Rule-based fallback ─────────────────────────────────────────
def _rule_based_analysis(data: dict) -> dict:
    """Deterministic heuristic analysis when no LLM is available."""

    tasks = data.get("tasks", [])
    stories = data.get("stories", [])
    projects = data.get("projects", [])
    escalations = data.get("escalations", [])
    risks = data.get("risks", [])
    members = data.get("members", [])

    # ── Compute metrics ──
    total_tasks = len(tasks)
    done_tasks = [t for t in tasks if t.get("status") == "Done"]
    in_prog = [t for t in tasks if t.get("status") == "In Progress"]
    todo_tasks = [t for t in tasks if t.get("status") == "To Do"]
    completion_rate = round(len(done_tasks) / total_tasks * 100, 1) if total_tasks else 0

    total_stories = len(stories)
    done_stories = [s for s in stories if s.get("status") == "Done"]
    story_completion = round(len(done_stories) / total_stories * 100, 1) if total_stories else 0

    delayed_tasks = [t for t in tasks if t.get("delay", 0) and int(str(t.get("delay", 0)).replace("d", "").strip() or 0) > 0]
    high_risk_stories = [s for s in stories if s.get("risk") in ("High", "Critical")]

    active_projects = [p for p in projects if p.get("status") == "Active"]
    critical_escalations = [e for e in escalations if e.get("severity") in ("Critical", "High")]

    # Top performers
    top_members = sorted(members, key=lambda m: m.get("overall", 0), reverse=True)[:3]
    low_members = sorted(members, key=lambda m: m.get("overall", 0))[:2]

    avg_alignment = round(sum(m.get("alignment", 0) for m in members) / len(members), 1) if members else 0

    # ── Chain of thought trace ──
    cot = (
        f"Step 1 — TASK ANALYSIS: {total_tasks} tasks total. "
        f"{len(done_tasks)} done ({completion_rate}%), {len(in_prog)} in progress, "
        f"{len(todo_tasks)} to do. {len(delayed_tasks)} tasks have delays.\n"
        f"Step 2 — STORY ANALYSIS: {total_stories} stories. "
        f"{len(done_stories)} completed ({story_completion}%). "
        f"{len(high_risk_stories)} stories flagged as high/critical risk.\n"
        f"Step 3 — SPRINT HEALTH: {len(active_projects)} active projects underway. "
        f"Task completion rate of {completion_rate}% indicates "
        f"{'healthy' if completion_rate >= 60 else 'needs attention'} sprint velocity.\n"
        f"Step 4 — PROJECT STATUS: {len(projects)} projects tracked. "
        f"{len(active_projects)} are active.\n"
        f"Step 5 — ESCALATION & RISK: {len(escalations)} escalations, "
        f"{len(critical_escalations)} critical/high. {len(risks)} active risks.\n"
        f"Step 6 — TEAM PERFORMANCE: {len(members)} members tracked. "
        f"Average alignment: {avg_alignment}%. "
        f"Top performers: {', '.join(m.get('name', '?') for m in top_members)}.\n"
        f"Step 7 — SYNTHESIS: Generating retrospective items based on analysis."
    )

    # ── Went well ──
    went_well = []
    if completion_rate >= 50:
        went_well.append(f"Task completion rate of {completion_rate}% — {len(done_tasks)} out of {total_tasks} tasks completed successfully.")
    if story_completion >= 30:
        went_well.append(f"Story delivery at {story_completion}% — {len(done_stories)} of {total_stories} backlog stories marked as Done.")
    if top_members:
        went_well.append(f"Strong individual performers: {', '.join(m.get('name', '?') + ' (' + str(m.get('overall', 0)) + '%)' for m in top_members)}.")
    if active_projects:
        went_well.append(f"{len(active_projects)} projects actively progressing with assigned PMs and team members.")
    if avg_alignment >= 75:
        went_well.append(f"Team alignment score averaging {avg_alignment}% across all members — indicating good JIRA-Git compliance.")
    if len(went_well) < 3:
        went_well.append("Cross-functional collaboration observed across PM, Dev, and QA roles in task distribution.")

    # ── Didn't go well ──
    didnt_go_well = []
    if delayed_tasks:
        delay_names = ", ".join(t.get("title", t.get("id", "?")) for t in delayed_tasks[:3])
        didnt_go_well.append(f"{len(delayed_tasks)} tasks experienced delays: {delay_names}.")
    if high_risk_stories:
        risk_names = ", ".join(s.get("id", "?") + " (" + s.get("title", "?") + ")" for s in high_risk_stories[:3])
        didnt_go_well.append(f"{len(high_risk_stories)} stories flagged as high/critical risk: {risk_names}.")
    if critical_escalations:
        didnt_go_well.append(f"{len(critical_escalations)} critical/high severity escalations raised during the sprint.")
    if completion_rate < 60:
        didnt_go_well.append(f"Overall task completion rate below target at {completion_rate}% — indicates sprint overcommitment.")
    if low_members and len(low_members) >= 2:
        didnt_go_well.append(f"Performance concerns for: {', '.join(m.get('name', '?') + ' (' + str(m.get('overall', 0)) + '%)' for m in low_members)}.")
    if todo_tasks:
        didnt_go_well.append(f"{len(todo_tasks)} tasks still in 'To Do' status at sprint review — capacity planning gap.")
    if len(didnt_go_well) < 3:
        didnt_go_well.append("Some task descriptions and assignments were incomplete, affecting sprint planning clarity.")

    # ── Improvements ──
    next_week = (datetime.utcnow() + timedelta(days=7)).strftime("%b %d, %Y")
    next_two_weeks = (datetime.utcnow() + timedelta(days=14)).strftime("%b %d, %Y")

    improvements = []
    if delayed_tasks:
        improvements.append({
            "action": "Conduct root-cause analysis on delayed tasks and re-estimate next sprint",
            "assignee": "Arjun Patel (PM)",
            "deadline": next_week,
            "priority": "High",
        })
    if high_risk_stories:
        improvements.append({
            "action": "Create mitigation plans for high-risk stories before next sprint starts",
            "assignee": "Sneha Iyer (Scrum Master)",
            "deadline": next_week,
            "priority": "High",
        })
    if critical_escalations:
        improvements.append({
            "action": "Review and resolve all open critical escalations in escalation triage meeting",
            "assignee": "Rajesh Mehta (CEO)",
            "deadline": next_week,
            "priority": "High",
        })
    improvements.append({
        "action": "Improve sprint capacity planning — compare story points committed vs delivered",
        "assignee": "Arjun Patel (PM)",
        "deadline": next_two_weeks,
        "priority": "Medium",
    })
    improvements.append({
        "action": "Schedule 1-on-1 coaching sessions for team members below performance threshold",
        "assignee": "Priya Sharma (HR)",
        "deadline": next_two_weeks,
        "priority": "Medium",
    })
    improvements.append({
        "action": "Enforce mandatory task description and assignee fields at creation time",
        "assignee": "Sneha Iyer (Scrum Master)",
        "deadline": next_week,
        "priority": "Low",
    })

    # ── AI Summary ──
    ai_summary = (
        f"Sprint retrospective analysis reveals a task completion rate of {completion_rate}% "
        f"with {len(done_tasks)} of {total_tasks} tasks delivered. "
        f"Story delivery stands at {story_completion}% across {total_stories} backlog items. "
        f"The sprint faced {len(critical_escalations)} critical escalations and "
        f"{len(high_risk_stories)} high-risk stories requiring attention. "
        f"Team alignment averages {avg_alignment}%, with top performers "
        f"{', '.join(m.get('name', '?') for m in top_members[:2])} leading delivery. "
        f"Key actions include root-cause analysis on delays, risk mitigation planning, "
        f"and improved capacity estimation for the next sprint cycle."
    )

    return {
        "chain_of_thought": cot,
        "went_well": went_well,
        "didnt_go_well": didnt_go_well,
        "improvements": improvements,
        "ai_summary": ai_summary,
    }


# ── Public API ───────────────────────────────────────────────────
async def run_sprint_retrospective() -> dict:
    """
    Main entry point.  Collects data → tries LLM with CoT → falls
    back to rule-based engine → returns structured retrospective.
    """
    data = await _collect_sprint_data()

    # Try LLM-based analysis first
    try:
        from ai_agents.llm_provider import get_llm
        get_llm()  # will raise RuntimeError if no key
        result = await _run_llm_analysis(data)
        result["source"] = "ai"
    except Exception as e:
        print(f"⚠️  LLM unavailable ({e}), using rule-based retrospective")
        result = _rule_based_analysis(data)
        result["source"] = "rule_based"

    return result
