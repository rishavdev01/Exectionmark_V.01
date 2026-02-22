from pydantic import BaseModel
from typing import Optional


class ExecutionWeek(BaseModel):
    id: str
    week: str
    health: int
    target: int


class SprintStatusSlice(BaseModel):
    id: str
    name: str
    value: int
    color: str


class CEOEscalation(BaseModel):
    id: int
    title: str
    severity: str
    project: str
    time: str
    status: str


class HealthFactor(BaseModel):
    id: str
    name: str
    weight: int
    score: int
    color: str


class StoryRisk(BaseModel):
    id: str
    title: str
    developer: str
    risk: int
    reason: str


class DevRiskContrib(BaseModel):
    id: str
    name: str
    riskScore: int
    storiesAtRisk: int
    avgDelay: str


class ActiveRisk(BaseModel):
    id: str
    storyId: str
    riskType: str
    riskLevel: str
    responsible: str
    desc: str


class EscalationEvent(BaseModel):
    id: int
    time: str
    event: str
    detail: str
    notified: str
    resolution: str
    severity: str


class RiskPattern(BaseModel):
    id: str
    title: str
    occurrences: int
    sprints: str
    impact: str
    recommendation: str
    color: str


class PerformanceMember(BaseModel):
    id: str
    name: str
    role: str
    alignment: int
    onTime: int
    rejection: int
    behaviour: float
    sprintContrib: int
    overall: float
    promotion: bool


class CEOImprovement(BaseModel):
    id: str
    action: str
    assignee: str
    deadline: str
    priority: str


class CEOBehaviourFeedback(BaseModel):
    id: str
    name: str
    communication: int
    ownership: int
    teamwork: int
    adaptability: int
    notes: str


class SaveBehaviourFeedback(BaseModel):
    """Request body for saving behaviour scores from Performance Insights."""
    name: str
    communication: int  # 1-10
    ownership: int
    teamwork: int
    adaptability: int
    notes: str = ""
