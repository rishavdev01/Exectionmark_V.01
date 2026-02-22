from pydantic import BaseModel
from typing import Optional


class PMWorkload(BaseModel):
    id: str
    name: str
    assigned: int
    completed: int
    pending: int
    overdue: int
    capacity: int


class PMEscalationEvent(BaseModel):
    id: str
    time: str
    event: str
    who: str
    status: str
    severity: str


class HighRiskMember(BaseModel):
    id: str
    name: str
    escalations: int
    avgDelay: str
    risk: str


class DelayDistribution(BaseModel):
    id: str
    range: str
    count: int


class PMRetroSummary(BaseModel):
    id: str
    sprintName: str
    completionPct: int
    alignmentAvg: float
    behaviourAvg: float
    bottleneck: str


class PMImprovement(BaseModel):
    """PM-specific: uses 'owner' and 'due' (NOT 'assignee'/'deadline' like CEO)"""
    id: str
    action: str
    owner: str
    due: str


class AIRetroSuggestion(BaseModel):
    id: str
    text: str
    sprint: str
