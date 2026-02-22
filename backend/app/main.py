"""
Exactiomark FastAPI application entry point.
All routers are registered here with their URL prefixes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth, dashboard, bugs,
    ceo, pm, lead, dev, devops, qa, hr,
    user_logins,
    users, employees, sprints, stories, tasks, projects,
    candidates, pipelines, deployments, system_health,
    alerts, reports, review_queue, escalations, ai_agent,
    companies,
)

app = FastAPI(title="Exactiomark API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Core routes ──
app.include_router(auth.router,         prefix="/api/auth",       tags=["Auth"])
app.include_router(dashboard.router,    prefix="/api/dashboard",  tags=["Dashboard"])
app.include_router(bugs.router,         prefix="/api/bugs",       tags=["Bugs"])

# ── UserLogin ──
app.include_router(user_logins.router,  prefix="/api/user-logins", tags=["UserLogins"])

# ── Feature Routers ──
app.include_router(users.router,         prefix="/api/users",         tags=["Users"])
app.include_router(employees.router,     prefix="/api/employees",     tags=["Employees"])
app.include_router(sprints.router,       prefix="/api/sprints",       tags=["Sprints"])
app.include_router(stories.router,       prefix="/api/stories",       tags=["Stories"])
app.include_router(tasks.router,         prefix="/api/tasks",         tags=["Tasks"])
app.include_router(projects.router,      prefix="/api/projects",      tags=["Projects"])
app.include_router(candidates.router,    prefix="/api/candidates",    tags=["Candidates"])
app.include_router(pipelines.router,     prefix="/api/pipelines",     tags=["Pipelines"])
app.include_router(deployments.router,   prefix="/api/deployments",   tags=["Deployments"])
app.include_router(system_health.router, prefix="/api/system-health", tags=["SystemHealth"])
app.include_router(alerts.router,        prefix="/api/alerts",        tags=["Alerts"])
app.include_router(reports.router,       prefix="/api/reports",       tags=["Reports"])
app.include_router(review_queue.router,  prefix="/api/review-queue",  tags=["ReviewQueue"])
app.include_router(escalations.router,   prefix="/api/escalations",   tags=["Escalations"])
app.include_router(ai_agent.router,      prefix="/api/ai",            tags=["AI"])

# ── Role-Specific Routers ──
app.include_router(ceo.router,          prefix="/api/ceo",         tags=["CEO"])
app.include_router(pm.router,           prefix="/api/pm",          tags=["PM"])
app.include_router(lead.router,         prefix="/api/lead",        tags=["Lead"])
app.include_router(dev.router,          prefix="/api/dev",         tags=["Developer"])
app.include_router(devops.router,       prefix="/api/devops",      tags=["DevOps"])
app.include_router(qa.router,           prefix="/api/qa",          tags=["QA"])
app.include_router(hr.router,           prefix="/api/hr",          tags=["HR"])
app.include_router(companies.router,    prefix="/api/companies",   tags=["Companies"])


@app.get("/")
async def root():
    return {"message": "Exactiomark API v2.0 — all systems nominal"}
