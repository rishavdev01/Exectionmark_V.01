"""
Tasks route — CRUD + role-based filtering + approval workflow
Maps to: CEOTasks, PMTasks (myTasks), TaskManagement, DevMyTasks, DevOpsTasksPage

Workflow:
  Dev/DevOps marks task "Done"  →  AI agent reviews  →  status becomes "In Review"
  Lead/PM clicks Approve        →  status becomes "Done"
  Lead/PM clicks Reject         →  status returns to "To Do" with rejection notes
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import tasks_collection

router = APIRouter()


class TaskCreate(BaseModel):
    id: str
    title: str
    description: str = ""
    assignedTo: str = ""
    from_user: str = ""
    to_user: str = ""
    priority: str = "Medium"
    status: str = "To Do"
    due: str = ""
    est: str = ""
    actual: str = "—"
    role: str = ""
    # ── Workflow tracking fields ──
    reviewedBy: str = ""
    approvedBy: str = ""
    reviewNotes: str = ""
    approvalNotes: str = ""
    reviewedAt: str = ""
    approvedAt: str = ""


@router.get("")
async def get_tasks(
    role: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    to_user: Optional[str] = Query(None),
    from_user: Optional[str] = Query(None),
):
    query = {}
    if role:
        query["role"] = role
    if status:
        query["status"] = status
    if to_user:
        query["to_user"] = to_user
    if from_user:
        query["from_user"] = from_user
    tasks = []
    async for t in tasks_collection.find(query, {"_id": 0}):
        tasks.append(t)
    return tasks


@router.get("/{task_id}")
async def get_task(task_id: str):
    task = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("")
async def create_task(body: dict):
    body.pop("_id", None)
    await tasks_collection.insert_one(body)
    return {"message": "Task created"}


@router.put("/{task_id}")
async def update_task(task_id: str, body: dict):
    body.pop("_id", None)
    result = await tasks_collection.update_one({"id": task_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    result = await tasks_collection.delete_one({"id": task_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}


# ══════════════════════════════════════════════════════════════════════════════
# Task Workflow Endpoints
# ══════════════════════════════════════════════════════════════════════════════

class MarkDoneRequest(BaseModel):
    markedBy: str = ""          # who clicked "Mark as Done"


class ApproveRequest(BaseModel):
    approvedBy: str = ""        # Lead / PM name
    approvalNotes: str = ""


class RejectRequest(BaseModel):
    rejectedBy: str = ""
    rejectionNotes: str = ""


@router.post("/{task_id}/mark-done")
async def mark_task_done(task_id: str, body: MarkDoneRequest = MarkDoneRequest()):
    """
    Dev/DevOps marks their task as done.
    1. Agent performs a lightweight review (alignment check).
    2. Status transitions to "In Review" (visible as transparent on Dev dashboard).
    3. Task appears in Lead/PM review queue for approval.
    """
    task = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    if not task:
        raise HTTPException(404, "Task not found")

    # ── Lightweight AI Agent review ──
    alignment = task.get("alignment", 0)
    title = task.get("title", task.get("story", ""))
    review_notes = []

    if alignment >= 80:
        review_notes.append(f"✅ High alignment ({alignment}%) — code changes are well-scoped.")
    elif alignment >= 60:
        review_notes.append(f"⚠️ Moderate alignment ({alignment}%) — minor scope drift detected.")
    else:
        review_notes.append(f"🔴 Low alignment ({alignment}%) — significant scope drift. Review carefully.")

    # Check basic completion signals
    actual = task.get("actual", "—")
    est = task.get("est", "")
    if actual != "—" and est:
        review_notes.append(f"Time tracking: estimated {est}, actual {actual}.")
    else:
        review_notes.append("⚠️ No actual time recorded — ensure time tracking is updated.")

    review_notes.append(f"Task '{title}' marked as done by {body.markedBy or 'Developer'}. Awaiting Lead/PM approval.")

    now = datetime.utcnow().isoformat()

    update_data = {
        "status": "In Review",
        "reviewedBy": "AI Agent",
        "reviewNotes": " | ".join(review_notes),
        "reviewedAt": now,
    }

    await tasks_collection.update_one({"id": task_id}, {"$set": update_data})

    updated = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    return {
        "message": "Task marked as done — now In Review",
        "task": updated,
        "review": {
            "reviewedBy": "AI Agent",
            "notes": review_notes,
            "reviewedAt": now,
        }
    }


@router.post("/{task_id}/approve")
async def approve_task(task_id: str, body: ApproveRequest = ApproveRequest()):
    """
    Lead/PM approves the task after reviewing.
    Status transitions from "In Review" to "Done".
    """
    task = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    if not task:
        raise HTTPException(404, "Task not found")

    if task.get("status") != "In Review":
        raise HTTPException(400, f"Task is not In Review (current status: {task.get('status')})")

    now = datetime.utcnow().isoformat()
    update_data = {
        "status": "Done",
        "approvedBy": body.approvedBy or "Lead",
        "approvalNotes": body.approvalNotes,
        "approvedAt": now,
    }

    await tasks_collection.update_one({"id": task_id}, {"$set": update_data})

    updated = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    return {"message": "Task approved", "task": updated}


@router.post("/{task_id}/reject")
async def reject_task(task_id: str, body: RejectRequest = RejectRequest()):
    """
    Lead/PM rejects the task.
    Status returns to "To Do" with rejection notes.
    """
    task = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    if not task:
        raise HTTPException(404, "Task not found")

    if task.get("status") != "In Review":
        raise HTTPException(400, f"Task is not In Review (current status: {task.get('status')})")

    update_data = {
        "status": "To Do",
        "approvedBy": "",
        "approvalNotes": f"Rejected by {body.rejectedBy or 'Lead'}: {body.rejectionNotes}",
        "approvedAt": "",
    }

    await tasks_collection.update_one({"id": task_id}, {"$set": update_data})

    updated = await tasks_collection.find_one({"id": task_id}, {"_id": 0})
    return {"message": "Task rejected — returned to To Do", "task": updated}
