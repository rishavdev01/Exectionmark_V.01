from pydantic import BaseModel
from typing import Optional, Union


class PullRequest(BaseModel):
    id: str
    title: str
    author: str
    branch: str
    base: str
    status: str
    reviewStatus: str
    comments: Union[int, list] = 0       # int (count) or list of {author, text, time}
    changedFiles: Optional[int] = 0
    additions: int
    deletions: int
    createdAt: Optional[str] = ""
    sprint: Optional[str] = ""
    # Frontend-expected fields
    story: Optional[str] = ""            # e.g. "ST-201 – Implement OAuth2 Login Flow"
    alignment: Optional[int] = 0         # AI alignment score 0-100
    ci: Optional[str] = "Pass"           # Pass | Fail
    files: Optional[int] = 0             # number of changed files
    aiRisk: Optional[str] = None         # AI risk note or null
    reviewer: Optional[str] = ""


class Branch(BaseModel):
    id: Union[str, int]
    name: str
    author: Optional[str] = ""
    status: Optional[str] = "Up to date"
    lastCommit: Optional[str] = ""
    commits: Optional[int] = 0
    aheadBy: Optional[int] = 0
    behindBy: Optional[int] = 0
    ciStatus: Optional[str] = "pass"
    sprint: Optional[str] = ""
    # Frontend-expected fields
    story: Optional[str] = ""            # e.g. "ST-201 – Implement OAuth2 Login Flow"
    aiRelevance: Optional[int] = 0       # AI relevance score 0-100
    aiNote: Optional[str] = ""           # AI note about the branch
    mergeReady: Optional[bool] = False
    conflicts: Optional[bool] = False


class Submission(BaseModel):
    id: str
    storyId: str
    title: str
    submittedBy: str
    submittedAt: str
    status: str
    reviewedBy: str
    tab: str
    aiScore: int
    comments: str = ""
