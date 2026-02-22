from pydantic import BaseModel
from typing import Optional


class BehaviourHistory(BaseModel):
    """HRBehaviourScores.jsx — history array: month, member, score, ratedBy"""
    id: str
    month: str          # e.g. 'Jan 2026'
    member: str
    score: float
    ratedBy: str


class BehaviourRating(BaseModel):
    """HRBehaviourScores.jsx criteria: communication, ownership, collaboration, leadership, discipline
    NOTE: 'collaboration' not 'teamwork' — verified from criteria array"""
    id: str
    member: str
    sprint: str
    communication: int  # 1–5
    ownership: int
    collaboration: int  # NOT 'teamwork'
    leadership: int
    discipline: int
    comment: str = ""
    ratedBy: str = ""


class Candidate(BaseModel):
    """HRInvitations.jsx"""
    id: int
    name: str
    email: str
    role: str
    dept: str
    project: str        # e.g. 'Sprint Beta' or '—'
    appliedDate: str
    status: str         # Screening | Interview | Offer Sent | Hired | Rejected
    experience: str     # e.g. '4 years'


class DeptPerformance(BaseModel):
    """HRPerformanceAnalytics.jsx"""
    id: str
    dept: str
    score: float


class SprintVelocity(BaseModel):
    """HRPerformanceAnalytics.jsx"""
    id: str
    sprint: str
    planned: int
    completed: int


class Performer(BaseModel):
    """HRPerformanceAnalytics.jsx — top + low performers"""
    id: str
    name: str
    score: float
    role: str
    issue: str = ""     # only for low performers
    type: str           # 'top' | 'low'


class AuditLog(BaseModel):
    """HRPromotions.jsx — auditLog: action, name, by, time"""
    id: str
    action: str
    name: str
    by: str
    time: str


class HRReport(BaseModel):
    """HRReports.jsx — no icon field (rendered client-side)"""
    id: int
    title: str
    desc: str
    color: str          # hex
    lastGenerated: str


class CompanyInfo(BaseModel):
    name: str
    domain: str
    industry: str
    location: str


class PerformanceWeights(BaseModel):
    sprint: int
    alignment: int
    delivery: int
    behaviour: int


class SprintPolicy(BaseModel):
    duration: int       # days
    maxSP: int
    approvalSLA: int    # hours


class CompanySettings(BaseModel):
    """HRCompanySettings.jsx — nested company{}, weights{}, sprintPolicy{}, access control lists"""
    id: str = "settings-001"
    company: CompanyInfo
    weights: PerformanceWeights
    sprintPolicy: SprintPolicy
    behaviourAssign: list[str]       # roles that can rate behaviour
    promotionWeightEdit: list[str]   # roles that can edit weights
