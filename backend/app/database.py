"""
Motor (async MongoDB) client and collection references.
Every collection listed in the implementation plan is defined here.
"""

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

# ── Core Collections ──
users_collection = db["users"]
employees_collection = db["employees"]
sprints_collection = db["sprints"]
stories_collection = db["stories"]
tasks_collection = db["tasks"]
projects_collection = db["projects"]

# ── Role-Specific Collections ──
candidates_collection = db["candidates"]
pipelines_collection = db["pipelines"]
deployments_collection = db["deployments"]
system_health_collection = db["system_health"]
alerts_collection = db["alerts"]
bugs_collection = db["bugs"]
reports_collection = db["reports"]
review_queue_collection = db["review_queue"]
escalations_collection = db["escalations"]

# ── AI ──
ai_results_collection = db["ai_results"]

# ── Task Activities (used by meeting_insights agent) ──
task_activities_collection = db["task_activities"]

# ── Teams (used by meeting_insights agent) ──
teams_collection = db["teams"]

# ── UserLogin ──
user_logins_collection = db["user_logins"]

# ── CEO Collections ──
execution_weeks_collection        = db["execution_weeks"]
sprint_status_slices_collection   = db["sprint_status_slices"]
ceo_escalations_collection        = db["ceo_escalations"]
health_factors_collection         = db["health_factors"]
story_risks_collection            = db["story_risks"]
dev_risk_contributions_collection = db["dev_risk_contributions"]
active_risks_collection           = db["active_risks"]
escalation_events_collection      = db["escalation_events"]
risk_patterns_collection          = db["risk_patterns"]
performance_members_collection    = db["performance_members"]
ceo_improvements_collection       = db["ceo_improvements"]
ceo_behaviour_feedback_collection = db["ceo_behaviour_feedback"]

# ── PM Collections ──
pm_workload_collection            = db["pm_workload"]
pm_escalation_events_collection   = db["pm_escalation_events"]
high_risk_members_collection      = db["high_risk_members"]
delay_distribution_collection     = db["delay_distribution"]
pm_retro_summary_collection       = db["pm_retro_summary"]
pm_improvements_collection        = db["pm_improvements"]
ai_retro_suggestions_collection   = db["ai_retro_suggestions"]

# ── Lead / Scrum Master Collections ──
sprint_stories_collection         = db["sprint_stories"]
lead_retrospectives_collection    = db["lead_retrospectives"]
# LeadDashboard.jsx
lead_team_members_collection      = db["lead_team_members"]
lead_workload_chart_collection    = db["lead_workload_chart"]
lead_perf_trend_collection        = db["lead_perf_trend"]
lead_review_queue_collection      = db["lead_review_queue"]
# SMAlignmentInsights.jsx
alignment_breakdown_collection    = db["alignment_breakdown"]
low_alignment_stories_collection  = db["low_alignment_stories"]
alignment_trend_collection        = db["alignment_trend"]
# SMMyTeam.jsx
team_members_detail_collection    = db["team_members_detail"]
# SMReviewQueue.jsx
review_queue_items_collection     = db["review_queue_items"]
# SMRiskBlockers.jsx
blockers_collection               = db["blockers"]
# SMTeamPerformance.jsx
member_perf_collection            = db["member_perf"]
sprint_trend_collection           = db["sprint_trend"]
# SMWorkload.jsx
sm_workload_collection            = db["sm_workload"]
workload_suggestions_collection   = db["workload_suggestions"]

# ── Developer Collections ──
pull_requests_collection          = db["pull_requests"]
branches_collection               = db["branches"]
submissions_collection            = db["submissions"]
progress_snapshots_collection     = db["progress_snapshots"]
dev_ai_feedback_collection        = db["dev_ai_feedback"]
dev_progress_history_collection   = db["dev_progress_history"]

# ── DevOps Collections ──
incidents_collection              = db["incidents"]
infra_changes_collection          = db["infra_changes"]
logs_alerts_collection            = db["logs_alerts"]
log_ai_analysis_collection        = db["log_ai_analysis"]
devops_tasks_collection           = db["devops_tasks"]
devops_ops_review_collection      = db["devops_ops_review"]

# ── QA Collections ──
test_cases_collection             = db["test_cases"]
bugs_qa_collection                = db["bugs_qa"]
assigned_stories_collection       = db["assigned_stories"]
regression_collection             = db["regression_suites"]
release_checks_collection         = db["release_checks"]
blocking_bugs_collection          = db["blocking_bugs"]
quality_metrics_collection        = db["quality_metrics"]
test_runs_collection              = db["test_runs"]
qa_reports_collection             = db["qa_reports"]

# ── HR Collections ──
behaviour_history_collection      = db["behaviour_history"]
behaviour_ratings_collection      = db["behaviour_ratings"]
dept_performance_collection       = db["dept_performance"]
sprint_velocity_collection        = db["sprint_velocity"]
performers_collection             = db["performers"]
audit_log_collection              = db["audit_log"]
hr_reports_collection             = db["hr_reports"]
company_settings_collection       = db["company_settings"]

# ── Companies (org-level, seeded in backend only) ──
companies_collection              = db["companies"]
