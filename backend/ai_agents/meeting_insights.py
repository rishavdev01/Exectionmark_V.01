"""
Agent 3 — Enterprise Meeting Insights & Verification (Chain-of-Thought)

Verifies meeting effectiveness by checking:
  - Attendance (participants vs. team members)
  - Transcript / notes analysis (LLM-driven agenda coverage)
  - Action items generated (extracted by LLM)
  - Follow-up tasks created (verified in internal DB)

Uses Chain-of-Thought (CoT) reasoning to produce a visible reasoning
trace, then a structured assessment.  Falls back to a rule-based
heuristic engine when no LLM is available.

Output includes:
  chain_of_thought: str   — visible step-by-step reasoning
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

from langchain_core.prompts import ChatPromptTemplate

from app.ai_agents.llm_provider import get_llm
from app.database import tasks_collection, task_activities_collection, teams_collection

# ── Scoring weights ──────────────────────────────────────────────
MEETING_WEIGHTS = {
    "attendance": 25,
    "agenda_match": 25,
    "action_items": 25,
    "tasks_created": 25,
}

# ── LLM prompts ─────────────────────────────────────────────────

# Prompt to extract structured meeting data from transcript/notes
EXTRACTION_PROMPT = """You are an expert Meeting Analysis AI agent for ExecSense.
Analyze the meeting transcript/notes and extract:

1. **attendees** — list of participant names mentioned
2. **agenda_items_covered** — list of agenda topics that were actually discussed
3. **action_items** — list of action items with fields: description, owner (if mentioned), deadline (if mentioned)
4. **key_decisions** — list of important decisions made
5. **risks_discussed** — list of risks, blockers, or concerns raised
6. **agenda_coverage_pct** — estimated percentage of planned agenda covered (0-100)
7. **summary** — concise executive summary of the meeting

Respond in valid JSON with exactly these keys:
attendees, agenda_items_covered, action_items, key_decisions,
risks_discussed, agenda_coverage_pct, summary.
"""

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", EXTRACTION_PROMPT),
    ("human", (
        "Meeting Title: {meeting_title}\n"
        "Project: {project_name}\n"
        "Expected Agenda: {expected_agenda}\n"
        "Team Members: {team_members}\n\n"
        "Meeting Notes / Transcript:\n{meeting_data}"
    )),
])

# Chain-of-Thought prompt for final narrative assessment
COT_ASSESSMENT_PROMPT = """You are an expert Meeting Effectiveness AI agent for ExecSense.
Given structured meeting data and verification results, perform analysis.

**You MUST think step-by-step before answering.**

## Chain-of-Thought Steps
1. ATTENDANCE CHECK — Compare actual attendees vs expected team members.
   Calculate attendance rate. Identify who was missing and if their
   absence impacts meeting outcomes.
2. AGENDA COVERAGE — Review agenda items covered vs planned.
   Calculate coverage percentage. Identify skipped topics and their
   importance. Note any off-topic discussions.
3. DECISION QUALITY — Assess quality and specificity of decisions made.
   Are they actionable? Do they have clear owners? Are they connected
   to project goals?
4. ACTION ITEMS ANALYSIS — Review action items for completeness.
   Check if each has an owner, deadline, and clear definition of done.
   Assess if follow-up tasks were created in the system.
5. EFFECTIVENESS SYNTHESIS — Based on steps 1-4, compute overall
   meeting effectiveness. Determine collaboration quality and project
   alignment. Generate specific recommendations.

## Output Format
Return ONLY valid JSON (no markdown fences) in this exact shape:
{
  "chain_of_thought": "<your step-by-step reasoning as a single string>",
  "effectiveness_score": <0-100>,
  "collaboration_score": <0-100>,
  "alignment_assessment": "LOW|MEDIUM|HIGH",
  "follow_up_risk": "LOW|MEDIUM|HIGH",
  "recommendations": ["<improvement 1>", "<improvement 2>", ...]
}

Be specific — reference actual attendee names, agenda items, and action items from the data.
"""

assessment_prompt = ChatPromptTemplate.from_messages([
    ("system", COT_ASSESSMENT_PROMPT),
    ("human", "Meeting Data:\n{meeting_data}"),
])


# ── Meeting Score Computation ────────────────────────────────────
def _compute_meeting_score(signals: dict[str, Any]) -> int:
    """Compute weighted meeting progress score (0–100)."""
    score = 0

    # Attendance (25 pts)
    expected_attendees = signals.get("expected_attendees", 0)
    actual_attendees = signals.get("actual_attendees", 0)
    if expected_attendees > 0:
        rate = min(actual_attendees / expected_attendees, 1.0)
        score += int(rate * MEETING_WEIGHTS["attendance"])
    elif actual_attendees > 0:
        score += MEETING_WEIGHTS["attendance"]

    # Agenda match (25 pts)
    agenda_coverage = signals.get("agenda_coverage_pct", 0)
    if agenda_coverage >= 80:
        score += MEETING_WEIGHTS["agenda_match"]
    elif agenda_coverage > 0:
        score += int((agenda_coverage / 100) * MEETING_WEIGHTS["agenda_match"])

    # Action items (25 pts)
    action_items_count = signals.get("action_items_count", 0)
    if action_items_count >= 3:
        score += MEETING_WEIGHTS["action_items"]
    elif action_items_count > 0:
        score += int((action_items_count / 3) * MEETING_WEIGHTS["action_items"])

    # Tasks created (25 pts)
    follow_up_tasks = signals.get("follow_up_tasks_created", 0)
    action_items = signals.get("action_items_count", 0)
    if action_items > 0 and follow_up_tasks > 0:
        rate = min(follow_up_tasks / action_items, 1.0)
        score += int(rate * MEETING_WEIGHTS["tasks_created"])
    elif follow_up_tasks > 0:
        score += MEETING_WEIGHTS["tasks_created"]

    return min(score, 100)


# ── Rule-based CoT fallback ─────────────────────────────────────
def _rule_based_meeting_analysis(
    signals: dict[str, Any],
    attendees: list[str],
    action_items: list[dict],
    key_decisions: list[str],
    risks: list[str],
    matched_attendees: list[str],
    unmatched_attendees: list[str],
    meeting_title: str,
    meeting_score: int,
    agenda_coverage: int,
    total_follow_ups: int,
) -> dict:
    """Deterministic heuristic analysis when no LLM is available."""

    expected = signals.get("expected_attendees", 0)
    actual = signals.get("actual_attendees", 0)
    att_rate = round(actual / expected * 100, 1) if expected > 0 else 100.0

    # ── Chain of thought trace ──
    cot = (
        f"Step 1 — ATTENDANCE CHECK: "
        f"{actual} attendee(s) present out of {expected} expected "
        f"(attendance rate: {att_rate}%). "
    )
    if matched_attendees:
        cot += f"Matched team members: {', '.join(matched_attendees[:5])}. "
    if unmatched_attendees:
        cot += f"Unknown attendees: {', '.join(unmatched_attendees[:3])}. "
    if att_rate < 70:
        cot += "⚠ Low attendance — meeting outcomes may lack buy-in. "

    cot += (
        f"\nStep 2 — AGENDA COVERAGE: "
        f"Agenda coverage estimated at {agenda_coverage}%. "
    )
    if agenda_coverage >= 80:
        cot += "Good coverage — most planned topics were discussed. "
    elif agenda_coverage >= 50:
        cot += "Moderate coverage — some topics were skipped. "
    else:
        cot += "⚠ Low coverage — significant agenda items were missed. "

    cot += (
        f"\nStep 3 — DECISION QUALITY: "
        f"{len(key_decisions)} decision(s) recorded. "
    )
    if key_decisions:
        cot += f"Decisions: {'; '.join(str(d)[:60] for d in key_decisions[:3])}. "
    else:
        cot += "⚠ No clear decisions recorded — meeting may lack actionable outcomes. "

    cot += (
        f"\nStep 4 — ACTION ITEMS: "
        f"{len(action_items)} action item(s) generated. "
        f"{total_follow_ups} follow-up task(s) created in the system. "
    )
    items_with_owner = sum(1 for i in action_items if i.get("owner"))
    items_with_deadline = sum(1 for i in action_items if i.get("deadline"))
    if action_items:
        cot += (
            f"{items_with_owner}/{len(action_items)} have owners, "
            f"{items_with_deadline}/{len(action_items)} have deadlines. "
        )
    if total_follow_ups < len(action_items) and action_items:
        cot += "⚠ Not all action items were converted to tasks. "

    # Effectiveness and risk
    effectiveness = meeting_score
    collaboration = min(100, int(att_rate * 0.5 + agenda_coverage * 0.3 + len(key_decisions) * 10))
    alignment = "HIGH" if agenda_coverage >= 80 else "MEDIUM" if agenda_coverage >= 50 else "LOW"
    follow_up_risk = "LOW"
    if total_follow_ups < len(action_items) * 0.5:
        follow_up_risk = "HIGH"
    elif total_follow_ups < len(action_items):
        follow_up_risk = "MEDIUM"

    cot += (
        f"\nStep 5 — EFFECTIVENESS SYNTHESIS: "
        f"Meeting score = {meeting_score}/100. "
        f"Collaboration = {collaboration}/100. "
        f"Alignment = {alignment}. "
        f"Follow-up risk = {follow_up_risk}."
    )

    recommendations = []
    if att_rate < 80:
        recommendations.append(f"Improve attendance — only {att_rate}% of expected attendees were present")
    if agenda_coverage < 70:
        recommendations.append("Better time management needed — enforce agenda timecboxes")
    if not key_decisions:
        recommendations.append("Ensure each meeting produces at least one clear, actionable decision")
    if items_with_owner < len(action_items):
        recommendations.append("Assign an owner to every action item before ending the meeting")
    if total_follow_ups < len(action_items):
        recommendations.append("Create follow-up tasks in the system for all action items")
    if not recommendations:
        recommendations.append("Meeting was effective — maintain the current format and cadence")

    return {
        "chain_of_thought": cot,
        "effectiveness_score": effectiveness,
        "collaboration_score": collaboration,
        "alignment_assessment": alignment,
        "follow_up_risk": follow_up_risk,
        "recommendations": recommendations,
    }


# ── Main Meeting Verification ───────────────────────────────────
async def verify_meeting_progress(
    meeting_title: str,
    project_name: str,
    meeting_data: str,
    project_id: str = "",
    company_id: str = "",
    task_id: str = "",
    expected_agenda: str = "",
    expected_attendees: Optional[list[str]] = None,
) -> dict[str, Any]:
    """
    Full enterprise meeting verification flow with Chain-of-Thought:
    1. Use LLM to extract structured data from transcript/notes
    2. Check attendance against team members from DB
    3. Check if follow-up tasks were created in DB
    4. Compute meeting score
    5. Run CoT assessment (LLM or rule-based fallback)
    """

    # ── 1 — Get team members from DB ──
    team_members_list: list[str] = []
    if project_id and company_id:
        try:
            team_docs = teams_collection.find({
                "project_id": project_id,
                "company_id": company_id,
            })
            async for team in team_docs:
                members = team.get("members", [])
                for m in members:
                    if isinstance(m, dict):
                        team_members_list.append(m.get("name", m.get("user_id", "")))
                    elif isinstance(m, str):
                        team_members_list.append(m)
        except Exception:
            pass

    if expected_attendees:
        team_members_list = list(set(team_members_list + expected_attendees))

    # ── 2 — LLM extraction from transcript/notes ──
    extracted = {}
    try:
        chain = extraction_prompt | get_llm()
        response = await chain.ainvoke({
            "meeting_title": meeting_title,
            "project_name": project_name,
            "expected_agenda": expected_agenda or "Not specified",
            "team_members": ", ".join(team_members_list) if team_members_list else "Not specified",
            "meeting_data": meeting_data,
        })
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0]
        extracted = json.loads(raw)
    except Exception:
        extracted = {
            "attendees": [],
            "agenda_items_covered": [],
            "action_items": [],
            "key_decisions": [],
            "risks_discussed": [],
            "agenda_coverage_pct": 0,
            "summary": "Could not extract meeting data",
        }

    # Parse extracted data
    attendees = extracted.get("attendees", [])
    action_items = extracted.get("action_items", [])
    agenda_coverage = extracted.get("agenda_coverage_pct", 0)
    key_decisions = extracted.get("key_decisions", [])
    risks = extracted.get("risks_discussed", [])

    # ── 3 — Attendance matching ──
    actual_count = len(attendees)
    expected_count = len(team_members_list) if team_members_list else actual_count

    matched_attendees = []
    unmatched_attendees = []
    if team_members_list:
        team_lower = {m.lower() for m in team_members_list}
        for att in attendees:
            if att.lower() in team_lower or any(att.lower() in t for t in team_lower):
                matched_attendees.append(att)
            else:
                unmatched_attendees.append(att)
    else:
        matched_attendees = attendees

    # ── 4 — Check for follow-up tasks created in DB ──
    follow_up_tasks_created = 0
    if project_id and company_id and task_id:
        try:
            meeting_task = await tasks_collection.find_one({"task_id": task_id})
            if meeting_task:
                created_at = meeting_task.get("created_at", datetime.utcnow())
                follow_up_tasks_created = await tasks_collection.count_documents({
                    "project_id": project_id,
                    "company_id": company_id,
                    "created_at": {"$gte": created_at},
                    "task_id": {"$ne": task_id},
                })
        except Exception:
            pass

    activity_follow_ups = 0
    if task_id:
        try:
            activity_follow_ups = await task_activities_collection.count_documents({
                "task_id": task_id,
                "activity_type": {"$in": ["task_created", "follow_up", "action_item"]},
            })
        except Exception:
            pass

    total_follow_ups = max(follow_up_tasks_created, activity_follow_ups)

    # ── 5 — Compute meeting score ──
    signals = {
        "expected_attendees": expected_count,
        "actual_attendees": actual_count,
        "matched_attendees": len(matched_attendees),
        "agenda_coverage_pct": agenda_coverage,
        "action_items_count": len(action_items),
        "follow_up_tasks_created": total_follow_ups,
        "decisions_count": len(key_decisions),
        "risks_count": len(risks),
    }
    meeting_score = _compute_meeting_score(signals)

    # ── 6 — CoT assessment: LLM first, fallback to rule-based ──
    assessment_data = json.dumps({
        "meeting_title": meeting_title,
        "attendees": attendees,
        "action_items": action_items,
        "key_decisions": key_decisions,
        "risks": risks,
        "agenda_coverage_pct": agenda_coverage,
        "follow_up_tasks": total_follow_ups,
        "meeting_score": meeting_score,
    }, indent=2, default=str)

    try:
        chain2 = assessment_prompt | get_llm()
        resp2 = await chain2.ainvoke({"meeting_data": assessment_data})
        raw2 = resp2.content.strip()
        if raw2.startswith("```"):
            raw2 = raw2.split("\n", 1)[-1].rsplit("```", 1)[0]
        llm_assessment = json.loads(raw2)
        llm_assessment["source"] = "ai"
    except Exception as e:
        print(f"⚠️  LLM unavailable for meeting analysis ({e}), using rule-based CoT")
        llm_assessment = _rule_based_meeting_analysis(
            signals, attendees, action_items, key_decisions, risks,
            matched_attendees, unmatched_attendees, meeting_title,
            meeting_score, agenda_coverage, total_follow_ups,
        )
        llm_assessment["source"] = "rule_based"

    # ── Build response ──
    chain_of_thought = llm_assessment.get("chain_of_thought", "")
    team_collaboration_score = llm_assessment.get("collaboration_score", meeting_score)
    ai_summary = llm_assessment.get("alignment_assessment", "Meeting analysis complete.")

    return {
        "meeting_score": meeting_score,
        "signals": signals,
        "attendance": {
            "expected": expected_count,
            "actual": actual_count,
            "matched": matched_attendees,
            "unmatched": unmatched_attendees,
            "attendance_rate": round(actual_count / expected_count * 100, 1) if expected_count else 100.0,
        },
        "agenda": {
            "coverage_pct": agenda_coverage,
            "items_covered": extracted.get("agenda_items_covered", []),
        },
        "action_items": {
            "count": len(action_items),
            "items": action_items,
        },
        "follow_up_tasks": {
            "created": total_follow_ups,
            "conversion_rate": round(total_follow_ups / len(action_items) * 100, 1) if action_items else 0.0,
        },
        "key_decisions": key_decisions,
        "risks_discussed": risks,
        "summary": extracted.get("summary", ""),
        "llm_assessment": llm_assessment,
        "weights": MEETING_WEIGHTS,
        "chain_of_thought": chain_of_thought,
        "source": llm_assessment.get("source", "unknown"),
        # ── Fields for LeadDashboard / CEO advisory ──
        "team_collaboration_score": team_collaboration_score,
        "ai_summary": ai_summary,
    }


# ── Legacy wrapper for backward-compat with supervisor ───────────
async def analyze_meeting(meeting_title: str, project_name: str, meeting_data: str) -> str:
    """Backward-compatible: runs LLM-only analysis when called via
    the old `meeting_insights` task type."""
    try:
        chain = extraction_prompt | get_llm()
        response = await chain.ainvoke({
            "meeting_title": meeting_title,
            "project_name": project_name,
            "expected_agenda": "Not specified",
            "team_members": "Not specified",
            "meeting_data": meeting_data,
        })
        return response.content
    except Exception:
        return json.dumps({
            "chain_of_thought": "Legacy analysis: LLM unavailable, returning basic assessment.",
            "summary": "Meeting analysis completed via rule-based engine.",
            "effectiveness_score": 50,
            "recommendations": ["Configure GOOGLE_API_KEY for full AI analysis"],
        })
