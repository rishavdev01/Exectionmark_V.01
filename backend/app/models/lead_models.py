"""
Lead / Scrum Master Pydantic models — all 9 pages, fields verified 1:1 against JSX.

Pages covered:
  LeadDashboard.jsx       → LeadTeamMember, LeadWorkloadEntry, LeadPerfTrend, LeadReviewItem
  SMSprintBoard.jsx       → SprintStory
  SMRetrospective.jsx     → LeadRetrospective  (wellNotes / didntNotes / actionNotes)
  SMAlignmentInsights.jsx → AlignmentBreakdown, LowAlignmentStory, AlignmentTrend
  SMMyTeam.jsx            → TeamMember  (nested sprintStories, alignmentHistory, workloadHistory)
  SMReviewQueue.jsx       → ReviewQueueItem  (story/developer/alignment/risk/submittedAt/aiNote)
  SMRiskBlockers.jsx      → Blocker  (id/story/title/blockerType/owner/daysBlocked/risk/resolved)
  SMTeamPerformance.jsx   → MemberPerf, SprintTrend
  SMWorkload.jsx          → WorkloadEntry, WorkloadSuggestion
"""

from pydantic import BaseModel
from typing import Optional, Union


# ── LeadDashboard.jsx ──────────────────────────────────────────────────────────
class LeadTeamMember(BaseModel):
    """teamMembers: id, name, role, tasks, completed, status"""
    id: int
    name: str
    role: str
    tasks: int
    completed: int
    status: str             # Active | On Leave


class LeadWorkloadEntry(BaseModel):
    """workloadData: name, assigned, completed"""
    id: str
    name: str
    assigned: int
    completed: int


class LeadPerfTrend(BaseModel):
    """perfTrend: week, score"""
    id: str
    week: str
    score: int


class LeadReviewItem(BaseModel):
    """reviewQueue: id, title, author, priority, submitted"""
    id: int
    title: str
    author: str
    priority: str           # High | Medium | Low
    submitted: str          # e.g. '2h ago'


# ── SMSprintBoard.jsx ──────────────────────────────────────────────────────────
class SprintStory(BaseModel):
    """
    SMSprintBoard.jsx initialStories:
    id, title, assignee, type, points, alignment, risk, reviewStatus, dueDate, status
    """
    id: str
    title: str
    assignee: str
    type: str               # Dev | DevOps | QA
    points: int
    alignment: int
    risk: str               # Low | Medium | High
    reviewStatus: str       # Pending | In Review | Approved | Rejected
    dueDate: str
    status: str             # To Do | In Progress | In Review | Done | Blocked
    sprint: str


# ── SMRetrospective.jsx ────────────────────────────────────────────────────────
class LeadRetrospective(BaseModel):
    """
    SMRetrospective.jsx: notes fields can be strings or lists depending on source.
    """
    id: str
    sprint: str
    wellNotes: Union[str, list] = ""
    didntNotes: Union[str, list] = ""
    actionNotes: Union[str, list] = ""
    aiSummary: str = ""


# ── SMAlignmentInsights.jsx ────────────────────────────────────────────────────
class AlignmentBreakdown(BaseModel):
    """alignmentBreakdown: name, keyword, filePath, semantic, scopeDrift"""
    id: str
    name: str
    keyword: int
    filePath: int
    semantic: int
    scopeDrift: int


class LowAlignmentStory(BaseModel):
    """lowAlignmentStories: id, title, developer, alignment, offenses, note"""
    id: str
    title: str
    developer: str
    alignment: int
    offenses: int
    note: str


class AlignmentTrend(BaseModel):
    """trendData: sprint, avg"""
    id: str
    sprint: str
    avg: int


# ── SMMyTeam.jsx ───────────────────────────────────────────────────────────────
class MiniStory(BaseModel):
    """nested sprintStories inside TeamMember: id, title, points, status, alignment"""
    id: str
    title: str
    points: int
    status: str
    alignment: int


class AlignmentHistoryPoint(BaseModel):
    """nested alignmentHistory: sprint, score"""
    sprint: str
    score: int


class WorkloadHistoryPoint(BaseModel):
    """nested workloadHistory: sprint, load"""
    sprint: str
    load: int


class TeamMember(BaseModel):
    """
    SMMyTeam.jsx teamData:
    id, name, role, avatar, activeStories, alignmentAvg, risk, workload, status,
    behaviourScore, sprintStories[], alignmentHistory[], rejectionRate,
    blockerInvolvement, behaviourNotes, workloadHistory[]
    """
    id: int
    name: str
    role: str
    avatar: str
    activeStories: int
    alignmentAvg: int
    risk: str               # Low | Medium | High
    workload: int
    status: str             # Active | On Leave
    behaviourScore: float
    sprintStories: list[MiniStory] = []
    alignmentHistory: list[AlignmentHistoryPoint] = []
    rejectionRate: int
    blockerInvolvement: int
    behaviourNotes: str
    workloadHistory: list[WorkloadHistoryPoint] = []


# ── SMReviewQueue.jsx ───────────────────────────────────────────────────────────
class ReviewQueueItem(BaseModel):
    """
    SMReviewQueue.jsx initialReviews:
    id, story, developer, alignment, risk, submittedAt, status, aiNote
    """
    id: str
    story: str
    developer: str
    alignment: int
    risk: str               # Low | Medium | High
    submittedAt: str        # e.g. '2h ago'
    status: str             # Pending | Approved | Changes Requested | Escalated to PM | Rejected
    aiNote: str


# ── SMRiskBlockers.jsx ──────────────────────────────────────────────────────────
class Blocker(BaseModel):
    """
    SMRiskBlockers.jsx initialBlockers:
    id, story, title, blockerType, owner, daysBlocked, risk, resolved
    """
    id: str
    story: str              # story ID e.g. 'ST-107'
    title: str              # story title
    blockerType: str        # Rejection Loop | DevOps Failure | Scope Drift | Approval Delay | Overload
    owner: str
    daysBlocked: int
    risk: str               # Low | Medium | High
    resolved: bool


# ── SMTeamPerformance.jsx ───────────────────────────────────────────────────────
class MemberPerf(BaseModel):
    """
    SMTeamPerformance.jsx memberPerf:
    name, completion, alignmentAvg, reviewDelayAvg, rejectionRate, behaviourScore
    """
    id: str
    name: str
    completion: int
    alignmentAvg: int
    reviewDelayAvg: str     # e.g. '1.2d'
    rejectionRate: int
    behaviourScore: float


class SprintTrend(BaseModel):
    """sprintTrend: sprint, completion, alignment, rejection"""
    id: str
    sprint: str
    completion: int
    alignment: int
    rejection: int


# ── SMWorkload.jsx ──────────────────────────────────────────────────────────────
class WorkloadEntry(BaseModel):
    """
    SMWorkload.jsx workloadData:
    name, stories, points, reviewLoad, capacity
    """
    id: str
    name: str
    stories: int
    points: int
    reviewLoad: int
    capacity: int


class WorkloadSuggestion(BaseModel):
    """suggestions: member, capacity, suggestion"""
    id: str
    member: str
    capacity: int
    suggestion: str
