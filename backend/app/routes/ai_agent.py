"""
AI Agent route — POST /api/ai/run — calls supervisor, stores results
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime
import traceback

from app.database import ai_results_collection

router = APIRouter()


class AIRunRequest(BaseModel):
    task_type: str
    payload: dict = {}


class AIRunResponse(BaseModel):
    task_type: str
    result: Any
    score: Optional[int] = None
    chain_of_thought: Optional[str] = None
    source: Optional[str] = None
    created_at: str


@router.post("/run")
async def run_ai_agent(body: AIRunRequest):
    """
    Runs the supervisor agent (LangGraph) end-to-end.
    Falls back to placeholder results if the supervisor fails.
    Returns the structured result with chain_of_thought reasoning.
    """
    try:
        from app.ai_agents.supervisor import run_supervisor

        # Try the real supervisor first
        chain_of_thought = ""
        source = "unknown"
        try:
            supervisor_output = await run_supervisor(body.task_type, body.payload)
            result = supervisor_output.get("result", supervisor_output)
            chain_of_thought = supervisor_output.get("chain_of_thought", "")
            source = supervisor_output.get("source", "ai")
        except Exception as supervisor_err:
            print(f"⚠️  Supervisor failed ({supervisor_err}), using placeholder")
            result = _get_placeholder_result(body.task_type)
            source = "placeholder"

        # Extract score from result
        score = 0
        if isinstance(result, dict):
            score = (
                result.get("score")
                or result.get("progress_score")
                or result.get("devops_score")
                or result.get("meeting_score")
                or result.get("qa_score")
                or result.get("research_score")
                or 0
            )

        # Store in DB
        record = {
            "task_type": body.task_type,
            "result": result,
            "score": score,
            "chain_of_thought": chain_of_thought,
            "source": source,
            "payload": body.payload,
            "created_at": datetime.utcnow().isoformat(),
        }
        await ai_results_collection.insert_one(record)

        return AIRunResponse(
            task_type=body.task_type,
            result=result,
            score=score,
            chain_of_thought=chain_of_thought,
            source=source,
            created_at=record["created_at"],
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def get_ai_results(task_type: Optional[str] = None, limit: int = 20):
    query = {}
    if task_type:
        query["task_type"] = task_type
    results = []
    cursor = ai_results_collection.find(query, {"_id": 0}).sort("created_at", -1).limit(limit)
    async for r in cursor:
        results.append(r)
    return results


def _get_placeholder_result(task_type: str) -> dict:
    """Return placeholder results matching frontend expectations per agent type."""
    placeholders = {
        "code_review": {
            "score": 92,
            "code_quality": {"score": 92, "issues": [], "suggestions": ["Memoize computeMetrics()"]},
            "security": {"vulnerabilities": []},
            "llm_assessment": "Code quality is high. No critical issues detected.",
        },
        "research_verification": {
            "score": 78,
            "research_score": 78,
            "citation_analysis": {"total": 5, "verified": 3, "quality": "HIGH"},
            "llm_assessment": {"summary": "Research is well-sourced.", "recommendations": []},
        },
        "meeting_insights": {
            "score": 82,
            "meeting_score": 82,
            "attendance": {"expected": 6, "actual": 5, "attendance_rate": 83.3},
            "agenda": {"coverage_pct": 85},
            "action_items": {"count": 4},
            "llm_assessment": {"effectiveness_score": 82, "recommendations": []},
        },
        "qa_verification": {
            "score": 85,
            "qa_score": 85,
            "coverage": {"percentage": 82, "meets_threshold": True},
            "bugs": {"open": 8, "closed": 14},
            "regression": {"detected": False},
            "ai_highlights": [
                {"text": "2 critical bugs in payment module remain open for 3+ days.", "type": "danger"},
                {"text": "Regression pass rate dropped to 78%.", "type": "warning"},
                {"text": "Test coverage improved to 82% this sprint.", "type": "success"},
            ],
            "llm_insights": {"quality_score": 85, "recommendations": []},
        },
        "cicd_analysis": {
            "score": 78,
            "devops_score": 78,
            "pipeline_analysis": {"total_runs": 4, "passed": 3, "failed": 1},
            "deployment_status": {"environment": "production", "status": "success"},
            "llm_assessment": {"summary": "Overall healthy CI/CD pipeline.", "recommendations": []},
        },
    }
    return placeholders.get(task_type, {"score": 0, "message": f"Unknown task type: {task_type}"})


@router.post("/retrospective")
async def run_retrospective():
    """
    Trigger the Sprint Retrospective AI Agent.
    Analyses all project/task/sprint data using chain-of-thought,
    stores structured results, and returns them.
    """
    from ai_agents.sprint_retrospective import run_sprint_retrospective
    from app.database import ceo_improvements_collection, ceo_behaviour_feedback_collection

    try:
        result = await run_sprint_retrospective()

        # Store went_well items
        went_well_docs = [
            {"category": "went_well", "text": item, "generated_at": datetime.utcnow().isoformat()}
            for item in result.get("went_well", [])
        ]
        # Store didnt_go_well items
        didnt_go_well_docs = [
            {"category": "didnt_go_well", "text": item, "generated_at": datetime.utcnow().isoformat()}
            for item in result.get("didnt_go_well", [])
        ]
        # Store improvement actions
        improvement_docs = [
            {
                "category": "improvement",
                "action": item.get("action", ""),
                "assignee": item.get("assignee", ""),
                "deadline": item.get("deadline", ""),
                "priority": item.get("priority", "Medium"),
                "generated_at": datetime.utcnow().isoformat(),
            }
            for item in result.get("improvements", [])
        ]

        # Clear old AI-generated retrospective data and insert new
        await ceo_improvements_collection.delete_many({"category": {"$in": ["went_well", "didnt_go_well", "improvement"]}})
        all_docs = went_well_docs + didnt_go_well_docs + improvement_docs
        if all_docs:
            await ceo_improvements_collection.insert_many(all_docs)

        # Store AI summary in behaviour feedback (update first doc or create)
        ai_summary = result.get("ai_summary", "")
        if ai_summary:
            existing = await ceo_behaviour_feedback_collection.find_one({})
            if existing:
                await ceo_behaviour_feedback_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"aiSummary": ai_summary}},
                )
            else:
                await ceo_behaviour_feedback_collection.insert_one({
                    "id": "retro-summary",
                    "name": "AI Retrospective",
                    "aiSummary": ai_summary,
                    "communication": 0,
                    "ownership": 0,
                    "teamwork": 0,
                    "adaptability": 0,
                    "notes": "",
                })

        return {
            "ok": True,
            "source": result.get("source", "unknown"),
            "chain_of_thought": result.get("chain_of_thought", ""),
            "went_well": result.get("went_well", []),
            "didnt_go_well": result.get("didnt_go_well", []),
            "improvements": result.get("improvements", []),
            "ai_summary": ai_summary,
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

