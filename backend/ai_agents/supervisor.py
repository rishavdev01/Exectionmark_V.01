"""
Supervisor Agent — LangGraph-based orchestrator.

Routes tasks to the appropriate specialist agent based on the task
type and aggregates results. Uses a LangGraph StateGraph to
coordinate the workflow:

    START → route_task → [specialist] → aggregate → END
"""

from __future__ import annotations

import json
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.ai_agents.github_code_analysis import analyze_code, verify_developer_progress
from app.ai_agents.cicd_log_parsing import analyze_cicd_logs, verify_devops_progress
from app.ai_agents.meeting_insights import analyze_meeting, verify_meeting_progress
from app.ai_agents.qa_test_verifier import verify_tests, verify_qa_progress
from app.ai_agents.document_ai_review import review_document, verify_research_progress

# ── Supported task types ─────────────────────────────────────────
TASK_TYPES = [
    "github_code_analysis",
    "dev_verification",
    "cicd_log_parsing",
    "devops_verification",
    "meeting_insights",
    "meeting_verification",
    "qa_test_verifier",
    "qa_verification",
    "document_ai_review",
    "research_verification",
]


# ── State schema ─────────────────────────────────────────────────
class SupervisorState(TypedDict):
    task_type: str
    input_data: dict[str, Any]
    agent_result: str
    final_output: dict[str, Any]


# ── Node functions ───────────────────────────────────────────────
async def route_task(state: SupervisorState) -> SupervisorState:
    """Validate & pass through — the conditional edge does actual routing."""
    task_type = state["task_type"]
    if task_type not in TASK_TYPES:
        state["agent_result"] = json.dumps(
            {"error": f"Unknown task type: {task_type}. Must be one of {TASK_TYPES}"}
        )
    return state


async def run_github_code_analysis(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await analyze_code(
        task_description=data.get("task_description", ""),
        code_data=data.get("code_data", ""),
    )
    state["agent_result"] = result
    return state


async def run_dev_verification(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await verify_developer_progress(
        github_token=data.get("github_token", ""),
        owner=data.get("owner", ""),
        repo=data.get("repo", ""),
        expected_branch=data.get("expected_branch", ""),
        expected_module=data.get("expected_module", ""),
        github_username=data.get("github_username", ""),
        task_description=data.get("task_description", ""),
    )
    state["agent_result"] = json.dumps(result, default=str)
    return state


async def run_cicd_log_parsing(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await analyze_cicd_logs(
        pipeline_name=data.get("pipeline_name", ""),
        log_data=data.get("log_data", ""),
    )
    state["agent_result"] = result
    return state


async def run_devops_verification(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await verify_devops_progress(
        github_token=data.get("github_token", ""),
        owner=data.get("owner", ""),
        repo=data.get("repo", ""),
        branch=data.get("branch", "main"),
        task_description=data.get("task_description", ""),
        environment=data.get("environment", "staging"),
    )
    state["agent_result"] = json.dumps(result, default=str)
    return state


async def run_meeting_insights(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await analyze_meeting(
        meeting_title=data.get("meeting_title", ""),
        project_name=data.get("project_name", ""),
        meeting_data=data.get("meeting_data", ""),
    )
    state["agent_result"] = result
    return state


async def run_meeting_verification(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await verify_meeting_progress(
        meeting_title=data.get("meeting_title", ""),
        project_name=data.get("project_name", ""),
        meeting_data=data.get("meeting_data", ""),
        project_id=data.get("project_id", ""),
        company_id=data.get("company_id", ""),
        task_id=data.get("task_id", ""),
        expected_agenda=data.get("expected_agenda", ""),
        expected_attendees=data.get("expected_attendees"),
    )
    state["agent_result"] = json.dumps(result, default=str)
    return state


async def run_qa_test_verifier(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await verify_tests(
        project_name=data.get("project_name", ""),
        task_description=data.get("task_description", ""),
        test_data=data.get("test_data", ""),
    )
    state["agent_result"] = result
    return state


async def run_qa_verification(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await verify_qa_progress(
        github_token=data.get("github_token", ""),
        owner=data.get("owner", ""),
        repo=data.get("repo", ""),
        branch=data.get("branch", "main"),
        task_description=data.get("task_description", ""),
        project_name=data.get("project_name", ""),
        project_id=data.get("project_id", ""),
        company_id=data.get("company_id", ""),
    )
    state["agent_result"] = json.dumps(result, default=str)
    return state


async def run_document_ai_review(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await review_document(
        project_name=data.get("project_name", ""),
        document_title=data.get("document_title", ""),
        document_content=data.get("document_content", ""),
    )
    state["agent_result"] = result
    return state


async def run_research_verification(state: SupervisorState) -> SupervisorState:
    data = state["input_data"]
    result = await verify_research_progress(
        document_title=data.get("document_title", ""),
        document_content=data.get("document_content", ""),
        task_description=data.get("task_description", ""),
        project_name=data.get("project_name", ""),
        validate_sources=data.get("validate_sources", True),
    )
    state["agent_result"] = json.dumps(result, default=str)
    return state


async def aggregate(state: SupervisorState) -> SupervisorState:
    """Parse agent result into structured output, propagating CoT fields."""
    raw = state.get("agent_result", "")
    try:
        # Try to extract JSON from the response (may contain markdown fences)
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[-1].rsplit("```", 1)[0]
        parsed = json.loads(clean)
    except (json.JSONDecodeError, IndexError):
        parsed = {"raw_response": raw}

    # Extract CoT fields from the parsed result
    chain_of_thought = ""
    source = "unknown"
    if isinstance(parsed, dict):
        chain_of_thought = parsed.get("chain_of_thought", "")
        source = parsed.get("source", "unknown")

    state["final_output"] = {
        "task_type": state["task_type"],
        "result": parsed,
        "chain_of_thought": chain_of_thought,
        "source": source,
    }
    return state


# ── Routing logic ────────────────────────────────────────────────
def _decide_agent(state: SupervisorState) -> str:
    """Conditional edge: pick the right specialist node."""
    type_map = {
        "github_code_analysis": "github_code_analysis",
        "dev_verification": "dev_verification",
        "cicd_log_parsing": "cicd_log_parsing",
        "devops_verification": "devops_verification",
        "meeting_insights": "meeting_insights",
        "meeting_verification": "meeting_verification",
        "qa_test_verifier": "qa_test_verifier",
        "qa_verification": "qa_verification",
        "document_ai_review": "document_ai_review",
        "research_verification": "research_verification",
    }
    return type_map.get(state["task_type"], "aggregate")


# ── Build the graph ──────────────────────────────────────────────
def build_supervisor_graph() -> StateGraph:
    graph = StateGraph(SupervisorState)

    # Add nodes
    graph.add_node("route_task", route_task)
    graph.add_node("github_code_analysis", run_github_code_analysis)
    graph.add_node("dev_verification", run_dev_verification)
    graph.add_node("cicd_log_parsing", run_cicd_log_parsing)
    graph.add_node("devops_verification", run_devops_verification)
    graph.add_node("meeting_insights", run_meeting_insights)
    graph.add_node("meeting_verification", run_meeting_verification)
    graph.add_node("qa_test_verifier", run_qa_test_verifier)
    graph.add_node("qa_verification", run_qa_verification)
    graph.add_node("document_ai_review", run_document_ai_review)
    graph.add_node("research_verification", run_research_verification)
    graph.add_node("aggregate", aggregate)

    # Entry
    graph.set_entry_point("route_task")

    # Conditional routing from route_task → specialist
    graph.add_conditional_edges(
        "route_task",
        _decide_agent,
        {
            "github_code_analysis": "github_code_analysis",
            "dev_verification": "dev_verification",
            "cicd_log_parsing": "cicd_log_parsing",
            "devops_verification": "devops_verification",
            "meeting_insights": "meeting_insights",
            "meeting_verification": "meeting_verification",
            "qa_test_verifier": "qa_test_verifier",
            "qa_verification": "qa_verification",
            "document_ai_review": "document_ai_review",
            "research_verification": "research_verification",
            "aggregate": "aggregate",  # fallback for unknown types
        },
    )

    # Each specialist → aggregate → END
    for agent_name in TASK_TYPES:
        graph.add_edge(agent_name, "aggregate")
    graph.add_edge("aggregate", END)

    return graph.compile()


# ── Public API ───────────────────────────────────────────────────
_compiled_graph = None


def get_supervisor():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_supervisor_graph()
    return _compiled_graph


async def run_supervisor(task_type: str, input_data: dict) -> dict:
    """Run the supervisor graph end-to-end and return final_output."""
    supervisor = get_supervisor()
    initial_state: SupervisorState = {
        "task_type": task_type,
        "input_data": input_data,
        "agent_result": "",
        "final_output": {},
    }
    result = await supervisor.ainvoke(initial_state)
    return result["final_output"]
