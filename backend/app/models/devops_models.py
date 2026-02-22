from pydantic import BaseModel
from typing import Optional


class Incident(BaseModel):
    """DevOpsIncidents.jsx — 'incident' is the description field (not 'title')"""
    id: str
    incident: str       # full incident description — NOT 'title'
    severity: str       # Critical | High | Medium | Low
    service: str
    openedAt: str
    resolvedAt: str
    rootCause: str
    mttd: str           # e.g. '8m'
    mttr: str           # e.g. '1h 45m'
    repeat: bool = False
    aiSummary: str


class InfraChange(BaseModel):
    """DevOpsInfrastructure.jsx — id is int, 'timestamp' not 'date', 'changedBy' not 'author'"""
    id: int
    type: str           # Docker Config Update | Kubernetes Scaling | Environment Variable | Terraform Modification
    service: str
    changedBy: str      # NOT 'author'
    timestamp: str      # NOT 'date'
    risk: str           # Low | Medium | High
    approved: bool
    details: str


class LogAlert(BaseModel):
    """DevOpsLogsAlerts.jsx — id is int, has 'count'"""
    id: int
    category: str       # Error | Warning | Security | Memory
    severity: str       # Critical | High | Medium | Low
    service: str
    message: str
    timestamp: str
    count: int = 1


class LogAIAnalysis(BaseModel):
    id: str
    text: str
    type: str           # danger | warning | success


class DevOpsTask(BaseModel):
    """DevOpsTasksPage.jsx — 'story' not 'title', ciAligned/deployTriggered/filesCorrect booleans"""
    id: int
    story: str          # NOT 'title'
    type: str           # Deployment | Infra Change | Monitoring Setup | Security Patch
    env: str            # Staging | Production | All | Dev
    status: str         # To Do | In Progress | Done
    alignment: int
    ciAligned: bool     # NOT 'ciAlign'
    deployTriggered: bool
    filesCorrect: bool
    aiNote: str
