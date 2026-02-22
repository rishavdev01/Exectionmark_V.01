from pydantic import BaseModel
from typing import Union, Optional


class TestCase(BaseModel):
    """QATestCases.jsx — 'steps' can be int (count) or list of step strings, 'story' is story name"""
    id: str
    title: str
    story: str
    type: str           # Functional | Negative | Integration | Performance | Boundary | Regression | UI
    priority: str       # Critical | High | Medium | Low
    status: str         # Pending | In Progress | Passed | Failed
    steps: Union[int, list] = 0  # number of steps or list of step strings
    expected: Optional[str] = ""
    assignee: Optional[str] = ""
    sprint: Optional[str] = ""
    updatedAt: Optional[str] = ""  # e.g. 'Feb 20'


class Bug(BaseModel):
    """QABugReports.jsx — 'assignedTo' not 'assignee', 'summary' not 'description', steps is list[str]"""
    id: str
    story: str
    severity: str       # Critical | High | Medium | Low
    status: str         # Open | In Progress | Resolved | Reopened
    assignedTo: str     # NOT 'assignee'
    reopenCount: int = 0
    summary: str        # NOT 'description'
    env: str            # Staging | Dev | Production
    steps: list[str]    # array of step strings — NOT int
    hasScreenshot: bool = False
    hasLogs: bool = False


class AssignedStory(BaseModel):
    """QAAssignedStories.jsx"""
    id: int
    story: str
    developer: str
    buildVersion: str
    alignment: int
    testStatus: str     # Pending | Testing | Passed | Failed
    priority: str
    deadline: str       # e.g. 'Feb 22'
    acceptance: list[str]
    linkedPR: str
    buildEnv: str       # Staging | Dev


class RegressionSuite(BaseModel):
    """QARegressionSuite.jsx — 'cases' not 'total', 'flaky' is bool"""
    id: str
    module: str
    cases: int          # NOT 'total'
    passed: int
    failed: int
    flaky: bool
    lastRun: str        # e.g. '2h ago'


class ReleaseCheck(BaseModel):
    """QAReleaseReadiness.jsx — 'label' not 'check', value can be str/int"""
    label: str          # NOT 'check'
    value: Union[int, str]
    threshold: Union[int, str]
    status: str         # pass | fail | warning


class BlockingBug(BaseModel):
    id: str
    summary: str
    severity: str
    service: str


class QualityMetric(BaseModel):
    """QAQualityMetrics.jsx — 'weight' is str like '40%', 'value' is int"""
    id: str
    label: str
    weight: str         # e.g. '40%' — stored as string
    value: int
    color: str          # hex color


class TestRun(BaseModel):
    """QATestRuns.jsx"""
    id: int
    build: str
    env: str
    total: int
    passed: int
    failed: int
    duration: str
    ciStatus: str
    coverage: int


class DataPoint(BaseModel):
    label: str
    value: str


class QAReport(BaseModel):
    """QAReports.jsx — icon is mapped by category on frontend"""
    id: int
    name: str
    color: str
    category: str         # Sprint | Bugs | Release | Regression
    description: str
    lastGenerated: str    # e.g. 'Feb 20, 2026'
    data: list[DataPoint]

