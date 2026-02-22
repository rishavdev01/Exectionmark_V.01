"""
Seed script — populates MongoDB with ALL hardcoded data from the 71 frontend pages.
Run: python -m app.seed
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def seed():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    # ── Drop existing collections ──
    for col_name in await db.list_collection_names():
        await db.drop_collection(col_name)
    print("🗑️  Cleared existing collections")

    # ═══════════════════════════════════════════════════════════════
    # 1. USERS  (from AuthContext.jsx — 7 users)
    # ═══════════════════════════════════════════════════════════════
    users = [
        {"id": "CEO001", "password": "ceo@123", "name": "Rajesh Mehta", "role": "CEO", "email": "rajesh@exactiomark.com", "department": "Executive", "avatar": "RM", "github_pat": ""},
        {"id": "HR001", "password": "hr@123", "name": "Priya Sharma", "role": "HR", "email": "priya@exactiomark.com", "department": "Human Resources", "avatar": "PS", "github_pat": ""},
        {"id": "PM001", "password": "pm@123", "name": "Arjun Patel", "role": "PM", "email": "arjun@exactiomark.com", "department": "Sprint Mgmt", "avatar": "AP", "github_pat": ""},
        {"id": "LEAD001", "password": "lead@123", "name": "Sneha Iyer", "role": "LEAD", "email": "sneha@exactiomark.com", "department": "Engineering", "avatar": "SI", "github_pat": ""},
        {"id": "DEV001", "password": "dev@123", "name": "Vikram Singh", "role": "DEVELOPER", "email": "vikram@exactiomark.com", "department": "Engineering", "avatar": "VS", "github_pat": ""},
        {"id": "OPS001", "password": "ops@123", "name": "Ananya Reddy", "role": "DEVOPS", "email": "ananya@exactiomark.com", "department": "Infrastructure", "avatar": "AR", "github_pat": ""},
        {"id": "QA001", "password": "qa@123", "name": "Divya Menon", "role": "QA", "email": "divya@exactiomark.com", "department": "Quality Assurance", "avatar": "DM", "github_pat": ""},
    ]
    await db.users.insert_many(users)
    print(f"✅  Seeded {len(users)} users")

    # ═══════════════════════════════════════════════════════════════
    # 2. EMPLOYEES (from employeeData.js — 8 employees)
    # ═══════════════════════════════════════════════════════════════
    employees = [
        {
            "id": "EMPDEV001", "name": "Vikram Singh", "role": "Developer", "dept": "Engineering", "avatar": "VS",
            "email": "vikram.singh@exactiomark.com", "phone": "+91 98765 43210",
            "projects": ["Sprint Alpha", "Sprint Beta"], "status": "Active",
            "perfScore": 89.2, "behaviour": 8.5, "risk": "Low", "sprintContrib": "24 SP",
            "alignment": 91, "onTime": 94, "rejection": 5,
            "alignmentHistory": [
                {"sprint": "S1", "score": 78}, {"sprint": "S2", "score": 82}, {"sprint": "S3", "score": 85},
                {"sprint": "S4", "score": 88}, {"sprint": "S5", "score": 90}, {"sprint": "S6", "score": 91},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 18}, {"sprint": "S2", "sp": 22}, {"sprint": "S3", "sp": 20},
                {"sprint": "S4", "sp": 24}, {"sprint": "S5", "sp": 21}, {"sprint": "S6", "sp": 26},
            ],
            "behaviourScores": {"communication": 9, "ownership": 9, "teamwork": 8, "leadership": 7, "discipline": 9},
            "managerComment": "Consistently delivers high-quality code. Excellent problem solver and proactive communicator.",
            "riskData": {"overloadFreq": 2, "escalationInvolvement": 1, "perfDrop": -3.2},
            "promotion": {"eligible": True, "aiVerdict": "Strongly Recommend", "managerReview": "Approved", "finalDecision": "Promoted", "lastReview": "Feb 15, 2026", "reviewedBy": "Priya Sharma"},
            "sprintTasks": 8, "workload": 72,
        },
        {
            "id": "EMPLEAD001", "name": "Sneha Iyer", "role": "Scrum Master", "dept": "Engineering", "avatar": "SI",
            "email": "sneha.iyer@exactiomark.com", "phone": "+91 98765 43211",
            "projects": ["Sprint Alpha"], "status": "Active",
            "perfScore": 86.8, "behaviour": 9.0, "risk": "Low", "sprintContrib": "18 SP",
            "alignment": 87, "onTime": 88, "rejection": 8,
            "alignmentHistory": [
                {"sprint": "S1", "score": 80}, {"sprint": "S2", "score": 83}, {"sprint": "S3", "score": 84},
                {"sprint": "S4", "score": 86}, {"sprint": "S5", "score": 85}, {"sprint": "S6", "score": 87},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 14}, {"sprint": "S2", "sp": 16}, {"sprint": "S3", "sp": 18},
                {"sprint": "S4", "sp": 17}, {"sprint": "S5", "sp": 19}, {"sprint": "S6", "sp": 18},
            ],
            "behaviourScores": {"communication": 9, "ownership": 8, "teamwork": 9, "leadership": 8, "discipline": 9},
            "managerComment": "Great facilitator. Improved code review throughput significantly this sprint.",
            "riskData": {"overloadFreq": 0, "escalationInvolvement": 0, "perfDrop": 1.5},
            "promotion": {"eligible": True, "aiVerdict": "Recommend", "managerReview": "Pending", "finalDecision": "—", "lastReview": "—", "reviewedBy": "—"},
            "sprintTasks": 5, "workload": 65,
        },
        {
            "id": "OPS001", "name": "Ananya Reddy", "role": "DevOps Engineer", "dept": "Infrastructure", "avatar": "AR",
            "email": "ananya.reddy@exactiomark.com", "phone": "+91 98765 43212",
            "projects": ["Sprint Alpha", "Sprint Gamma"], "status": "Active",
            "perfScore": 74.3, "behaviour": 7.5, "risk": "High", "sprintContrib": "21 SP",
            "alignment": 78, "onTime": 72, "rejection": 15,
            "alignmentHistory": [
                {"sprint": "S1", "score": 82}, {"sprint": "S2", "score": 80}, {"sprint": "S3", "score": 78},
                {"sprint": "S4", "score": 76}, {"sprint": "S5", "score": 75}, {"sprint": "S6", "score": 78},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 20}, {"sprint": "S2", "sp": 22}, {"sprint": "S3", "sp": 25},
                {"sprint": "S4", "sp": 23}, {"sprint": "S5", "sp": 20}, {"sprint": "S6", "sp": 21},
            ],
            "behaviourScores": {"communication": 7, "ownership": 8, "teamwork": 7, "leadership": 6, "discipline": 8},
            "managerComment": "Technically strong but workload management needs support. Needs better task estimation.",
            "riskData": {"overloadFreq": 5, "escalationInvolvement": 3, "perfDrop": -7.8},
            "promotion": {"eligible": False, "aiVerdict": "Not Recommended", "managerReview": "Hold", "finalDecision": "Hold", "lastReview": "Feb 14, 2026", "reviewedBy": "Arjun Patel"},
            "sprintTasks": 7, "workload": 92,
        },
        {
            "id": "PM001", "name": "Arjun Patel", "role": "Sprint Master", "dept": "Management", "avatar": "AP",
            "email": "arjun.patel@exactiomark.com", "phone": "+91 98765 43213",
            "projects": ["Sprint Alpha"], "status": "Active",
            "perfScore": 85.5, "behaviour": 8.8, "risk": "Low", "sprintContrib": "—",
            "alignment": 85, "onTime": 90, "rejection": 6,
            "alignmentHistory": [
                {"sprint": "S1", "score": 80}, {"sprint": "S2", "score": 82}, {"sprint": "S3", "score": 84},
                {"sprint": "S4", "score": 83}, {"sprint": "S5", "score": 86}, {"sprint": "S6", "score": 85},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 0}, {"sprint": "S2", "sp": 0}, {"sprint": "S3", "sp": 0},
                {"sprint": "S4", "sp": 0}, {"sprint": "S5", "sp": 0}, {"sprint": "S6", "sp": 0},
            ],
            "behaviourScores": {"communication": 9, "ownership": 9, "teamwork": 9, "leadership": 8, "discipline": 9},
            "managerComment": "Excellent sprint management skills. Keeps team motivated and aligned.",
            "riskData": {"overloadFreq": 1, "escalationInvolvement": 2, "perfDrop": 0.5},
            "promotion": {"eligible": True, "aiVerdict": "Recommend", "managerReview": "Approved", "finalDecision": "Pending", "lastReview": "Feb 18, 2026", "reviewedBy": "Rajesh Mehta"},
            "sprintTasks": 0, "workload": 55,
        },
        {
            "id": "EMPHR001", "name": "Priya Sharma", "role": "HR Manager", "dept": "Human Resources", "avatar": "PS",
            "email": "priya.sharma@exactiomark.com", "phone": "+91 98765 43214",
            "projects": ["—"], "status": "Active",
            "perfScore": 88.1, "behaviour": 9.2, "risk": "Low", "sprintContrib": "—",
            "alignment": 82, "onTime": 95, "rejection": 3,
            "alignmentHistory": [
                {"sprint": "S1", "score": 75}, {"sprint": "S2", "score": 78}, {"sprint": "S3", "score": 80},
                {"sprint": "S4", "score": 81}, {"sprint": "S5", "score": 83}, {"sprint": "S6", "score": 82},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 0}, {"sprint": "S2", "sp": 0}, {"sprint": "S3", "sp": 0},
                {"sprint": "S4", "sp": 0}, {"sprint": "S5", "sp": 0}, {"sprint": "S6", "sp": 0},
            ],
            "behaviourScores": {"communication": 10, "ownership": 9, "teamwork": 9, "leadership": 9, "discipline": 9},
            "managerComment": "Outstanding HR leadership. Drives culture and process improvements.",
            "riskData": {"overloadFreq": 0, "escalationInvolvement": 0, "perfDrop": 2.1},
            "promotion": {"eligible": True, "aiVerdict": "Strongly Recommend", "managerReview": "Approved", "finalDecision": "Promoted", "lastReview": "Feb 12, 2026", "reviewedBy": "Rajesh Mehta"},
            "sprintTasks": 0, "workload": 50,
        },
        {
            "id": "EMPDEV002", "name": "Rahul Verma", "role": "Developer", "dept": "Engineering", "avatar": "RV",
            "email": "rahul.verma@exactiomark.com", "phone": "+91 98765 43215",
            "projects": ["Sprint Beta"], "status": "Probation",
            "perfScore": 72.1, "behaviour": 6.8, "risk": "Medium", "sprintContrib": "14 SP",
            "alignment": 70, "onTime": 68, "rejection": 18,
            "alignmentHistory": [
                {"sprint": "S1", "score": 75}, {"sprint": "S2", "score": 72}, {"sprint": "S3", "score": 70},
                {"sprint": "S4", "score": 68}, {"sprint": "S5", "score": 71}, {"sprint": "S6", "score": 70},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 12}, {"sprint": "S2", "sp": 10}, {"sprint": "S3", "sp": 14},
                {"sprint": "S4", "sp": 11}, {"sprint": "S5", "sp": 13}, {"sprint": "S6", "sp": 14},
            ],
            "behaviourScores": {"communication": 6, "ownership": 7, "teamwork": 7, "leadership": 5, "discipline": 7},
            "managerComment": "Needs improvement on code quality and delivery timelines. Frequent rework cycles.",
            "riskData": {"overloadFreq": 3, "escalationInvolvement": 2, "perfDrop": -5.4},
            "promotion": {"eligible": False, "aiVerdict": "Not Recommended", "managerReview": "Hold", "finalDecision": "Hold", "lastReview": "Feb 10, 2026", "reviewedBy": "Sneha Iyer"},
            "sprintTasks": 6, "workload": 58,
        },
        {
            "id": "EMPQA001", "name": "Meera Nair", "role": "QA Engineer", "dept": "Quality", "avatar": "MN",
            "email": "meera.nair@exactiomark.com", "phone": "+91 98765 43216",
            "projects": ["Sprint Alpha"], "status": "Active",
            "perfScore": 81.4, "behaviour": 8.0, "risk": "Low", "sprintContrib": "16 SP",
            "alignment": 83, "onTime": 85, "rejection": 7,
            "alignmentHistory": [
                {"sprint": "S1", "score": 78}, {"sprint": "S2", "score": 80}, {"sprint": "S3", "score": 81},
                {"sprint": "S4", "score": 82}, {"sprint": "S5", "score": 84}, {"sprint": "S6", "score": 83},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 12}, {"sprint": "S2", "sp": 14}, {"sprint": "S3", "sp": 15},
                {"sprint": "S4", "sp": 14}, {"sprint": "S5", "sp": 16}, {"sprint": "S6", "sp": 16},
            ],
            "behaviourScores": {"communication": 8, "ownership": 8, "teamwork": 8, "leadership": 7, "discipline": 8},
            "managerComment": "Thorough testing approach. Good eye for edge cases. Growing into leadership.",
            "riskData": {"overloadFreq": 1, "escalationInvolvement": 0, "perfDrop": 1.2},
            "promotion": {"eligible": True, "aiVerdict": "Recommend", "managerReview": "Pending", "finalDecision": "—", "lastReview": "—", "reviewedBy": "—"},
            "sprintTasks": 4, "workload": 60,
        },
        {
            "id": "EMPDEV003", "name": "Karan Joshi", "role": "Developer", "dept": "Engineering", "avatar": "KJ",
            "email": "karan.joshi@exactiomark.com", "phone": "+91 98765 43217",
            "projects": ["Sprint Gamma"], "status": "On Leave",
            "perfScore": 68.5, "behaviour": 7.2, "risk": "High", "sprintContrib": "10 SP",
            "alignment": 65, "onTime": 62, "rejection": 20,
            "alignmentHistory": [
                {"sprint": "S1", "score": 72}, {"sprint": "S2", "score": 70}, {"sprint": "S3", "score": 68},
                {"sprint": "S4", "score": 66}, {"sprint": "S5", "score": 64}, {"sprint": "S6", "score": 65},
            ],
            "sprintTrend": [
                {"sprint": "S1", "sp": 14}, {"sprint": "S2", "sp": 12}, {"sprint": "S3", "sp": 11},
                {"sprint": "S4", "sp": 10}, {"sprint": "S5", "sp": 9}, {"sprint": "S6", "sp": 10},
            ],
            "behaviourScores": {"communication": 7, "ownership": 7, "teamwork": 7, "leadership": 5, "discipline": 7},
            "managerComment": "Performance declining. Currently on leave. Need 1-on-1 after return.",
            "riskData": {"overloadFreq": 4, "escalationInvolvement": 3, "perfDrop": -9.1},
            "promotion": {"eligible": False, "aiVerdict": "Not Recommended", "managerReview": "Hold", "finalDecision": "Hold", "lastReview": "Feb 8, 2026", "reviewedBy": "Sneha Iyer"},
            "sprintTasks": 3, "workload": 45,
        },
    ]
    await db.employees.insert_many(employees)
    print(f"✅  Seeded {len(employees)} employees")

    # ═══════════════════════════════════════════════════════════════
    # 3. SPRINTS (from SprintOverview.jsx + PMDashboard)
    # ═══════════════════════════════════════════════════════════════
    sprints = [
        {"id": "SP-01", "name": "Sprint Alpha", "status": "Active", "startDate": "Feb 10, 2026", "endDate": "Feb 24, 2026", "velocity": 87, "storyPoints": 42, "completion": 68, "health": "Healthy", "daysLeft": 3, "totalStories": 12, "completedStories": 8},
        {"id": "SP-02", "name": "Sprint Beta", "status": "Planning", "startDate": "Feb 24, 2026", "endDate": "Mar 10, 2026", "velocity": 0, "storyPoints": 35, "completion": 0, "health": "Healthy", "daysLeft": 14, "totalStories": 10, "completedStories": 0},
        {"id": "SP-03", "name": "Sprint Gamma", "status": "Completed", "startDate": "Jan 27, 2026", "endDate": "Feb 10, 2026", "velocity": 92, "storyPoints": 48, "completion": 100, "health": "Healthy", "daysLeft": 0, "totalStories": 15, "completedStories": 15},
        {"id": "SP-04", "name": "Sprint Delta", "status": "Active", "startDate": "Feb 12, 2026", "endDate": "Feb 26, 2026", "velocity": 78, "storyPoints": 38, "completion": 45, "health": "At Risk", "daysLeft": 5, "totalStories": 10, "completedStories": 4},
        {"id": "SP-05", "name": "Sprint Epsilon", "status": "Planning", "startDate": "Feb 28, 2026", "endDate": "Mar 14, 2026", "velocity": 0, "storyPoints": 0, "completion": 0, "health": "Healthy", "daysLeft": 14, "totalStories": 0, "completedStories": 0},
    ]
    await db.sprints.insert_many(sprints)
    print(f"✅  Seeded {len(sprints)} sprints")

    # ═══════════════════════════════════════════════════════════════
    # 4. STORIES (from PMTasks.jsx + BacklogStories.jsx)
    # ═══════════════════════════════════════════════════════════════
    stories = [
        {"id": "ST-101", "title": "Implement Auth Module", "assignee": "Vikram Singh", "type": "Dev", "alignment": 94, "risk": "Low", "approval": "Approved", "delay": 0, "est": "8h", "actual": "7.5h", "status": "Done", "sprint_id": "SP-01", "priority": "High", "storyPoints": 5},
        {"id": "ST-102", "title": "Setup CI/CD Pipeline", "assignee": "Ananya Reddy", "type": "DevOps", "alignment": 78, "risk": "High", "approval": "Pending", "delay": 6, "est": "12h", "actual": "16h", "status": "In Progress", "sprint_id": "SP-01", "priority": "High", "storyPoints": 8},
        {"id": "ST-103", "title": "User Profile API", "assignee": "Vikram Singh", "type": "Dev", "alignment": 88, "risk": "Low", "approval": "Approved", "delay": 0, "est": "6h", "actual": "5h", "status": "In Review", "sprint_id": "SP-01", "priority": "Medium", "storyPoints": 3},
        {"id": "ST-104", "title": "Dashboard UI Redesign", "assignee": "Rahul Verma", "type": "Dev", "alignment": 65, "risk": "High", "approval": "Pending", "delay": 12, "est": "10h", "actual": "18h", "status": "In Progress", "sprint_id": "SP-01", "priority": "High", "storyPoints": 5},
        {"id": "ST-105", "title": "Integration Tests – Sprint API", "assignee": "Meera Nair", "type": "QA", "alignment": 85, "risk": "Low", "approval": "Approved", "delay": 0, "est": "4h", "actual": "4h", "status": "Done", "sprint_id": "SP-01", "priority": "Medium", "storyPoints": 3},
        {"id": "ST-106", "title": "Database Migration Script", "assignee": "Ananya Reddy", "type": "DevOps", "alignment": 72, "risk": "Medium", "approval": "Pending", "delay": 3, "est": "5h", "actual": "7h", "status": "In Progress", "sprint_id": "SP-01", "priority": "Medium", "storyPoints": 3},
        {"id": "ST-107", "title": "Notification Service", "assignee": "Karan Joshi", "type": "Dev", "alignment": 58, "risk": "High", "approval": "Rejected", "delay": 18, "est": "8h", "actual": "—", "status": "To Do", "sprint_id": "SP-02", "priority": "High", "storyPoints": 5},
        {"id": "ST-108", "title": "Load Testing Setup", "assignee": "Meera Nair", "type": "QA", "alignment": 90, "risk": "Low", "approval": "Approved", "delay": 0, "est": "6h", "actual": "5.5h", "status": "Done", "sprint_id": "SP-01", "priority": "Low", "storyPoints": 2},
        {"id": "ST-109", "title": "API Rate Limiting", "assignee": "Vikram Singh", "type": "Dev", "alignment": 82, "risk": "Low", "approval": "In Review", "delay": 0, "est": "4h", "actual": "—", "status": "In Review", "sprint_id": "SP-01", "priority": "Medium", "storyPoints": 3},
        {"id": "ST-110", "title": "Monitoring Dashboard", "assignee": "Ananya Reddy", "type": "DevOps", "alignment": 70, "risk": "Medium", "approval": "Pending", "delay": 4, "est": "10h", "actual": "—", "status": "To Do", "sprint_id": "SP-02", "priority": "Medium", "storyPoints": 5},
    ]
    await db.stories.insert_many(stories)
    print(f"✅  Seeded {len(stories)} stories")

    # ═══════════════════════════════════════════════════════════════
    # 5. TASKS (from PMTasks myTasks + CEOTasks + TaskManagement)
    # ═══════════════════════════════════════════════════════════════
    tasks = [
        # PM tasks from CEO
        {"id": "T-101", "title": "Finalize Q2 Sprint Roadmap", "description": "Review and approve the product roadmap for Q2 sprints with milestone dates.", "assignedTo": "Arjun Patel (Project Manager)", "from_user": "Rajesh Mehta (CEO)", "to_user": "Arjun Patel", "priority": "High", "status": "In Progress", "due": "Feb 22", "est": "8h", "actual": "5h", "role": "PM"},
        {"id": "T-102", "title": "Prepare Board Presentation", "description": "Create executive summary for board meeting on company growth metrics.", "assignedTo": "Arjun Patel (Project Manager)", "from_user": "Rajesh Mehta (CEO)", "to_user": "Arjun Patel", "priority": "Critical", "status": "To Do", "due": "Feb 25", "est": "6h", "actual": "—", "role": "PM"},
        {"id": "T-103", "title": "Review Resource Allocation", "description": "Analyze team utilization and approve reallocations as needed for next sprint.", "assignedTo": "Arjun Patel (Project Manager)", "from_user": "Rajesh Mehta (CEO)", "to_user": "Arjun Patel", "priority": "Medium", "status": "Done", "due": "Feb 18", "est": "4h", "actual": "4h", "role": "PM"},
        {"id": "T-104", "title": "Update Client Demo Environment", "description": "Deploy latest features to the client demo environment for stakeholder review.", "assignedTo": "Arjun Patel (Project Manager)", "from_user": "Rajesh Mehta (CEO)", "to_user": "Arjun Patel", "priority": "High", "status": "In Progress", "due": "Feb 24", "est": "5h", "actual": "3h", "role": "PM"},
        {"id": "T-105", "title": "Quarterly Risk Report", "description": "Compile and present the quarterly risk assessment report to leadership.", "assignedTo": "Arjun Patel (Project Manager)", "from_user": "Rajesh Mehta (CEO)", "to_user": "Arjun Patel", "priority": "Medium", "status": "To Do", "due": "Mar 01", "est": "4h", "actual": "—", "role": "PM"},
        # CEO tasks
        {"id": "T-201", "title": "Review Q1 Financial Report", "description": "Analyze and approve the Q1 financial performance report before stakeholder distribution.", "assignedTo": "Rajesh Mehta (CEO)", "from_user": "System", "to_user": "Rajesh Mehta", "priority": "High", "status": "In Progress", "due": "Feb 25", "est": "4h", "actual": "2h", "role": "CEO"},
        {"id": "T-202", "title": "Approve Sprint Beta Plan", "description": "Review the Sprint Beta plan submitted by PM and approve milestones and resource allocation.", "assignedTo": "Rajesh Mehta (CEO)", "from_user": "Arjun Patel", "to_user": "Rajesh Mehta", "priority": "High", "status": "To Do", "due": "Feb 23", "est": "2h", "actual": "—", "role": "CEO"},
        {"id": "T-203", "title": "Investor Meeting Prep", "description": "Prepare slides, financial summaries, and growth metrics for upcoming investor meeting.", "assignedTo": "Rajesh Mehta (CEO)", "from_user": "System", "to_user": "Rajesh Mehta", "priority": "Critical", "status": "To Do", "due": "Feb 28", "est": "6h", "actual": "—", "role": "CEO"},
        # Developer tasks
        {"id": "T-301", "title": "Fix login page bug", "description": "Resolve the login page rendering issue reported by QA team in Sprint Alpha.", "assignedTo": "Vikram Singh (Developer)", "from_user": "Sneha Iyer", "to_user": "Vikram Singh", "priority": "High", "status": "In Progress", "due": "Feb 22", "est": "3h", "actual": "1h", "role": "DEVELOPER"},
        {"id": "T-302", "title": "Implement user settings API", "description": "Create RESTful API endpoints for user settings with proper validation and error handling.", "assignedTo": "Vikram Singh (Developer)", "from_user": "Arjun Patel", "to_user": "Vikram Singh", "priority": "Medium", "status": "To Do", "due": "Feb 24", "est": "6h", "actual": "—", "role": "DEVELOPER"},
        {"id": "T-303", "title": "Code review: Auth module", "description": "Perform thorough code review of the authentication module for security best practices.", "assignedTo": "Vikram Singh (Developer)", "from_user": "Sneha Iyer", "to_user": "Vikram Singh", "priority": "Low", "status": "Done", "due": "Feb 20", "est": "2h", "actual": "1.5h", "role": "DEVELOPER"},
        {"id": "T-304", "title": "Write unit tests for Profile API", "description": "Write comprehensive unit tests covering all edge cases for the Profile API endpoints.", "assignedTo": "Vikram Singh (Developer)", "from_user": "Arjun Patel", "to_user": "Vikram Singh", "priority": "Medium", "status": "In Progress", "due": "Feb 23", "est": "4h", "actual": "2h", "role": "DEVELOPER"},
    ]
    await db.tasks.insert_many(tasks)
    print(f"✅  Seeded {len(tasks)} tasks")

    # ═══════════════════════════════════════════════════════════════
    # 6. PROJECTS (from CEOProjects.jsx)
    # ═══════════════════════════════════════════════════════════════
    projects = [
        {"id": "P-01", "name": "ExecSense Platform", "description": "AI-powered executive dashboard for real-time sprint tracking, risk analysis, and team performance insights.", "client": "Internal", "sprint": "Sprint 3", "assignedPM": "Arjun Patel", "members": 4, "createdDate": "Jan 15, 2026", "budget": "₹25L", "burnRate": "₹3.2L/mo", "status": "Active", "lead": "Arjun Patel", "team": ["Vikram Singh", "Ananya Reddy", "Meera Nair"], "timeline": "Jan 2026 – Jun 2026", "completion": 42, "health": "Healthy"},
        {"id": "P-02", "name": "Client Portal v2", "description": "Redesigned client portal with self-service features, analytics dashboards, and real-time project status updates.", "client": "Nexus Corp", "sprint": "Sprint 2", "assignedPM": "Sneha Iyer", "members": 3, "createdDate": "Feb 01, 2026", "budget": "₹12L", "burnRate": "₹1.5L/mo", "status": "Active", "lead": "Sneha Iyer", "team": ["Rahul Verma", "Karan Joshi"], "timeline": "Feb 2026 – May 2026", "completion": 15, "health": "At Risk"},
        {"id": "P-03", "name": "Internal Tools Suite", "description": "Suite of internal productivity tools including time tracking, leave management, and resource allocation.", "client": "Internal", "sprint": "Sprint 1", "assignedPM": "Vikram Singh", "members": 2, "createdDate": "Feb 10, 2026", "budget": "₹8L", "burnRate": "₹0.8L/mo", "status": "Active", "lead": "Vikram Singh", "team": ["Meera Nair"], "timeline": "Mar 2026 – Jul 2026", "completion": 0, "health": "Healthy"},
    ]
    await db.projects.insert_many(projects)
    print(f"✅  Seeded {len(projects)} projects")

    # ═══════════════════════════════════════════════════════════════
    # 7. CANDIDATES (from CEOHiring + HRInvitations)
    # ═══════════════════════════════════════════════════════════════
    candidates = [
        {"id": 1, "name": "Amit Desai", "email": "amit.desai@gmail.com", "role": "Developer", "status": "Screening", "dept": "Engineering", "project": "Sprint Alpha", "appliedDate": "Feb 14, 2026", "experience": "4 yrs", "match": 92, "source": "Referral"},
        {"id": 2, "name": "Neha Kapoor", "email": "neha.k@gmail.com", "role": "QA Engineer", "status": "Screening", "dept": "Quality Assurance", "project": "Sprint Beta", "appliedDate": "Feb 16, 2026", "experience": "3 yrs", "match": 85, "source": "LinkedIn"},
        {"id": 3, "name": "Rohan Mehta", "email": "rohan.m@gmail.com", "role": "DevOps", "status": "Screening", "dept": "Infrastructure", "project": "Sprint Alpha", "appliedDate": "Feb 17, 2026", "experience": "5 yrs", "match": 88, "source": "Job Portal"},
        {"id": 4, "name": "Kavita Rao", "email": "kavita.r@gmail.com", "role": "Developer", "status": "Rejected", "dept": "Engineering", "project": "Sprint Gamma", "appliedDate": "Feb 12, 2026", "experience": "2 yrs", "match": 65, "source": "Campus"},
        {"id": 5, "name": "Suresh Nair", "email": "suresh.n@gmail.com", "role": "Lead", "status": "Screening", "dept": "Engineering", "project": "Sprint Delta", "appliedDate": "Feb 18, 2026", "experience": "7 yrs", "match": 95, "source": "Referral"},
        {"id": 6, "name": "Lakshmi Venkat", "email": "lakshmi.v@gmail.com", "role": "Developer", "status": "Screening", "dept": "Engineering", "project": "Sprint Beta", "appliedDate": "Feb 19, 2026", "experience": "3 yrs", "match": 78, "source": "LinkedIn"},
        {"id": 7, "name": "Deepak Gupta", "email": "deepak.g@gmail.com", "role": "QA Engineer", "status": "Screening", "dept": "Quality Assurance", "project": "Sprint Alpha", "appliedDate": "Feb 15, 2026", "experience": "4 yrs", "match": 90, "source": "Job Portal"},
        {"id": 8, "name": "Ravi Kumar", "email": "ravi.kumar@gmail.com", "role": "Developer", "status": "Interview", "dept": "Engineering", "project": "Sprint Beta", "appliedDate": "Feb 15, 2026", "experience": "4 years", "match": 82, "source": "Job Portal"},
        {"id": 9, "name": "Nisha Patel", "email": "nisha.patel@gmail.com", "role": "DevOps", "status": "Screening", "dept": "Infrastructure", "project": "", "appliedDate": "Feb 12, 2026", "experience": "3 years", "match": 79, "source": "LinkedIn"},
        {"id": 10, "name": "Aakash Gupta", "email": "aakash.gupta@gmail.com", "role": "QA Engineer", "status": "Offer Sent", "dept": "Quality Assurance", "project": "Sprint Beta", "appliedDate": "Feb 10, 2026", "experience": "5 years", "match": 91, "source": "Referral"},
        {"id": 11, "name": "Lakshmi Rao", "email": "lakshmi.rao@gmail.com", "role": "HR Manager", "status": "Hired", "dept": "Human Resources", "project": "", "appliedDate": "Feb 8, 2026", "experience": "7 years", "match": 96, "source": "Referral"},
    ]
    await db.candidates.insert_many(candidates)
    print(f"✅  Seeded {len(candidates)} candidates")

    # ═══════════════════════════════════════════════════════════════
    # 8. PIPELINES (from DevOpsDashboard.jsx)
    # ═══════════════════════════════════════════════════════════════
    pipelines = [
        {"id": 1, "name": "Build – Auth Service", "status": "Passed", "branch": "main", "duration": "2m 34s", "triggered": "10 min ago"},
        {"id": 2, "name": "Deploy – Staging", "status": "Running", "branch": "develop", "duration": "—", "triggered": "3 min ago"},
        {"id": 3, "name": "Test Suite – Sprint API", "status": "Failed", "branch": "feature/sprint-api", "duration": "4m 12s", "triggered": "22 min ago"},
        {"id": 4, "name": "Build – Notification Svc", "status": "Passed", "branch": "main", "duration": "1m 58s", "triggered": "45 min ago"},
    ]
    await db.pipelines.insert_many(pipelines)
    print(f"✅  Seeded {len(pipelines)} pipelines")

    # ═══════════════════════════════════════════════════════════════
    # 9. DEPLOYMENTS (from DevOpsDashboard.jsx)
    # ═══════════════════════════════════════════════════════════════
    deployments = [
        {"id": 1, "service": "Auth Service", "env": "Production", "version": "v2.4.1", "time": "Today, 09:30", "status": "Success"},
        {"id": 2, "service": "Sprint API", "env": "Staging", "version": "v1.8.0-rc.2", "time": "Today, 08:15", "status": "Success"},
        {"id": 3, "service": "Notification Svc", "env": "Production", "version": "v1.2.3", "time": "Yesterday, 17:45", "status": "Rollback"},
    ]
    await db.deployments.insert_many(deployments)
    print(f"✅  Seeded {len(deployments)} deployments")

    # ═══════════════════════════════════════════════════════════════
    # 10. SYSTEM HEALTH (from DevOpsDashboard.jsx)
    # ═══════════════════════════════════════════════════════════════
    system_health = [
        {"service": "Auth Service", "cpu": 32, "memory": 58, "uptime": 99.98},
        {"service": "Sprint API", "cpu": 45, "memory": 72, "uptime": 99.95},
        {"service": "Notification Svc", "cpu": 18, "memory": 34, "uptime": 99.88},
        {"service": "Database (MongoDB)", "cpu": 55, "memory": 81, "uptime": 99.99},
    ]
    await db.system_health.insert_many(system_health)
    print(f"✅  Seeded {len(system_health)} system health records")

    # ═══════════════════════════════════════════════════════════════
    # 11. ALERTS (from DevOpsDashboard.jsx)
    # ═══════════════════════════════════════════════════════════════
    alerts = [
        {"id": 1, "msg": "High memory usage on Sprint API (72%)", "level": "warning", "time": "5 min ago"},
        {"id": 2, "msg": "Test Suite failed on feature/sprint-api", "level": "error", "time": "22 min ago"},
        {"id": 3, "msg": "Auto-scaling triggered for Auth Service", "level": "info", "time": "1 hour ago"},
        {"id": 4, "msg": "SSL cert expiry in 14 days", "level": "warning", "time": "3 hours ago"},
    ]
    await db.alerts.insert_many(alerts)
    print(f"✅  Seeded {len(alerts)} alerts")

    # ═══════════════════════════════════════════════════════════════
    # 12. BUGS (from QADashboard.jsx)
    # ═══════════════════════════════════════════════════════════════
    bugs = [
        {"id": 1, "name": "Login redirect loop", "status": "Open", "priority": "High", "assignee": "Vikram Singh", "description": "Users get stuck in redirect loop after login", "color": "#ef4444"},
        {"id": 2, "name": "Dashboard chart not rendering", "status": "Open", "priority": "Medium", "assignee": "Rahul Verma", "description": "Bar chart fails to render on slow connections", "color": "#ef4444"},
        {"id": 3, "name": "Sprint API 500 error", "status": "In Progress", "priority": "Critical", "assignee": "Ananya Reddy", "description": "Intermittent 500 errors on /api/sprints", "color": "#f59e0b"},
        {"id": 4, "name": "Notification delay", "status": "In Progress", "priority": "Low", "assignee": "Karan Joshi", "description": "Email notifications delayed by 2+ hours", "color": "#f59e0b"},
        {"id": 5, "name": "Profile image upload crash", "status": "Resolved", "priority": "Medium", "assignee": "Vikram Singh", "description": "Large image uploads cause browser crash", "color": "#10b981"},
        {"id": 6, "name": "Date picker incorrect format", "status": "Resolved", "priority": "Low", "assignee": "Meera Nair", "description": "Date picker shows US format instead of ISO", "color": "#10b981"},
        {"id": 7, "name": "Role-based access bypass", "status": "Open", "priority": "Critical", "assignee": "Vikram Singh", "description": "Non-admin users can access admin routes", "color": "#ef4444"},
        {"id": 8, "name": "Memory leak in websocket", "status": "Reopened", "priority": "High", "assignee": "Ananya Reddy", "description": "WebSocket connections not properly closed", "color": "#8b5cf6"},
    ]
    await db.bugs.insert_many(bugs)
    print(f"✅  Seeded {len(bugs)} bugs")

    # ═══════════════════════════════════════════════════════════════
    # 13. REPORTS (from ReportsPage.jsx, CEOReports.jsx)
    # ═══════════════════════════════════════════════════════════════
    reports = [
        {"id": 1, "title": "Sprint Report", "type": "Sprint", "date": "Feb 20, 2026", "role": "all", "desc": "Weekly sprint progress and velocity report", "lastGenerated": "Feb 20, 2026"},
        {"id": 2, "title": "Performance Report", "type": "Performance", "date": "Feb 18, 2026", "role": "all", "desc": "Team performance metrics and alignment scores", "lastGenerated": "Feb 18, 2026"},
        {"id": 3, "title": "Budget Report", "type": "Budget", "date": "Feb 15, 2026", "role": "CEO", "desc": "Project budget utilization and burn rate analysis", "lastGenerated": "Feb 15, 2026"},
        {"id": 4, "title": "Risk Report", "type": "Risk", "date": "Feb 19, 2026", "role": "all", "desc": "Risk assessment and escalation summary", "lastGenerated": "Feb 19, 2026"},
        {"id": 5, "title": "Quality Report", "type": "Quality", "date": "Feb 17, 2026", "role": "QA", "desc": "Test coverage, bug trends, and quality metrics", "lastGenerated": "Feb 17, 2026"},
        {"id": 6, "title": "HR Analytics Report", "type": "HR", "date": "Feb 16, 2026", "role": "HR", "desc": "Employee engagement, hiring funnel, behaviour scores", "lastGenerated": "Feb 16, 2026"},
    ]
    await db.reports.insert_many(reports)
    print(f"✅  Seeded {len(reports)} reports")

    # ═══════════════════════════════════════════════════════════════
    # 14. REVIEW QUEUE (from PMReviewQueue.jsx)
    # ═══════════════════════════════════════════════════════════════
    review_queue = [
        {"id": "ST-103", "task": "User Profile API", "submittedBy": "Vikram Singh", "alignment": 88, "leadApproval": "Approved", "delay": 0, "risk": "Low", "aiComment": "Code quality is high. Alignment within expected range."},
        {"id": "ST-102", "task": "Setup CI/CD Pipeline", "submittedBy": "Ananya Reddy", "alignment": 78, "leadApproval": "Pending", "delay": 6, "risk": "High", "aiComment": "Significant delay detected. Pipeline config has 3 unresolved warnings."},
        {"id": "ST-109", "task": "API Rate Limiting", "submittedBy": "Vikram Singh", "alignment": 82, "leadApproval": "Approved", "delay": 0, "risk": "Low", "aiComment": "Implementation follows best practices. Ready for merge."},
        {"id": "ST-104", "task": "Dashboard UI Redesign", "submittedBy": "Rahul Verma", "alignment": 65, "leadApproval": "Rejected", "delay": 12, "risk": "High", "aiComment": "Alignment below threshold. 3 components deviate from design spec."},
        {"id": "ST-106", "task": "Database Migration Script", "submittedBy": "Ananya Reddy", "alignment": 72, "leadApproval": "Pending", "delay": 3, "risk": "Medium", "aiComment": "Migration plan covers 80% of schemas. Missing rollback strategy."},
        {"id": "ST-110", "task": "Monitoring Dashboard", "submittedBy": "Ananya Reddy", "alignment": 70, "leadApproval": "Pending", "delay": 4, "risk": "Medium", "aiComment": "Partially complete. Needs integration with alerting service."},
    ]
    await db.review_queue.insert_many(review_queue)
    print(f"✅  Seeded {len(review_queue)} review queue items")

    # ═══════════════════════════════════════════════════════════════
    # 15. ESCALATIONS (from PMRiskEscalation.jsx)
    # ═══════════════════════════════════════════════════════════════
    escalations = [
        {"time": "Feb 20, 2026 10:30", "event": "Sprint Delta — deployment failure escalated", "who": "Ananya Reddy", "status": "Open", "severity": "High"},
        {"time": "Feb 19, 2026 15:00", "event": "Design spec mismatch — Dashboard UI", "who": "Rahul Verma", "status": "In Progress", "severity": "Medium"},
        {"time": "Feb 18, 2026 09:15", "event": "CI/CD pipeline broken for 4 hours", "who": "Ananya Reddy", "status": "Resolved", "severity": "High"},
        {"time": "Feb 17, 2026 14:45", "event": "Dependency conflict in Auth module", "who": "Vikram Singh", "status": "Resolved", "severity": "Low"},
        {"time": "Feb 16, 2026 11:00", "event": "Scope creep in Sprint Beta", "who": "Sneha Iyer", "status": "Resolved", "severity": "Medium"},
    ]
    await db.escalations.insert_many(escalations)
    print(f"✅  Seeded {len(escalations)} escalations")

    # ═══════════════════════════════════════════════════════════════
    # NEW PAGE-SPECIFIC COLLECTIONS
    # ═══════════════════════════════════════════════════════════════

    # ── Retrospectives ──
    retrospectives = [
        {
            "id": "retro-ceo-s12", "role": "CEO", "sprint": "Sprint 12",
            "wentWell": [
                "API Gateway migration completed on time",
                "Zero critical bugs in production this sprint",
                "Team collaboration improved significantly",
            ],
            "didntGoWell": [
                "Code review cycle took too long (avg 2.8 days)",
                "Two stories moved to next sprint due to scope creep",
                "Daily standups consistently ran over",
            ],
            "improvements": [
                "Implement 24-hour code review SLA",
                "Break large stories into sub-tasks before sprint start",
                "Time-box standups to 15 minutes",
            ],
            "aiSummary": "Sprint 12 showed strong delivery discipline with API migration success. Primary blockers were process-related — review latency and scope management. Recommend targeting code review SLA as the highest-impact improvement.",
            "behaviourFeedback": [
                {"member": "Vikram Singh", "score": 9.2, "note": "Excellent delivery and proactive blocker resolution."},
                {"member": "Sneha Iyer", "score": 8.8, "note": "Strong facilitation; team velocity improved."},
                {"member": "Ananya Reddy", "score": 9.0, "note": "Zero downtime this sprint — exceptional infra work."},
            ],
        },
        {
            "id": "retro-pm-s12", "role": "PM", "sprint": "Sprint 12",
            "wentWell": ["Sprint goal met", "Stakeholder communication improved", "Review queue cleared 95%"],
            "didntGoWell": ["Two stories missed acceptance criteria", "Velocity dropped by 8%"],
            "improvements": ["Tighten story acceptance criteria review", "Add mid-sprint sync checkpoint"],
            "aiSuggestions": [
                {"type": "Process", "text": "Add Definition of Ready checklist before sprint planning."},
                {"type": "Communication", "text": "Weekly stakeholder update email to reduce ad-hoc requests."},
            ],
        },
        {
            "id": "retro-lead-s12", "role": "LEAD", "sprint": "Sprint 12",
            "wellNotes": ["Team delivered 94% of committed SP", "Code review quality improved"],
            "didntNotes": ["Two blockers went unresolved for 3+ days", "Test coverage dipped to 76%"],
            "actionNotes": ["Daily blocker triage at 9am", "QA to flag coverage gaps in sprint planning"],
            "aiSummary": "Sprint 12 was strong overall. Key risk: slow blocker resolution. Recommend empowering devs to self-resolve L1 blockers.",
        },
    ]
    await db.retrospectives.insert_many(retrospectives)
    print(f"✅  Seeded {len(retrospectives)} retrospectives")

    # ── Risk Items ──
    risk_items = [
        {"id": "RSK-001", "title": "API Gateway Overload", "severity": "High", "status": "Active", "owner": "Ananya Reddy", "type": "Performance", "description": "CPU spikes to 94% during peak load.", "resolution": "Scale horizontally by end of week.", "sprint": "Sprint 12", "role": "CEO"},
        {"id": "RSK-002", "title": "Auth Token Expiry Bug", "severity": "Critical", "status": "Active", "owner": "Vikram Singh", "type": "Security", "description": "Tokens not refreshing in Safari.", "resolution": "Hotfix in review.", "sprint": "Sprint 12", "role": "CEO"},
        {"id": "RSK-003", "title": "Release Pipeline Failures", "severity": "Medium", "status": "Monitoring", "owner": "Ananya Reddy", "type": "CI/CD", "description": "2 out of 5 recent deployments failed.", "resolution": "Updated base Docker image.", "sprint": "Sprint 12", "role": "CEO"},
        {"id": "BLK-001", "title": "DB Migration Script Failing", "severity": "High", "status": "Open", "owner": "Vikram Singh", "type": "blocker", "description": "Migration script for v3 schema failing on staging.", "impact": "Blocks 3 stories.", "sprint": "Sprint 12", "role": "LEAD"},
        {"id": "BLK-002", "title": "Third-party API Rate Limit", "severity": "Medium", "status": "In Progress", "owner": "Arjun Patel", "type": "dependency", "description": "Payment gateway API rate-limited us.", "impact": "Delays payment feature by 2 days.", "sprint": "Sprint 12", "role": "LEAD"},
    ]
    await db.risk_items.insert_many(risk_items)
    print(f"✅  Seeded {len(risk_items)} risk items")

    # ── Sprint Boards ──
    sprint_boards = [
        {"id": "SB-001", "storyId": "STR-101", "title": "Implement OAuth2 Login", "assignee": "Vikram Singh", "points": 5, "priority": "High", "status": "In Progress", "risk": "Low", "alignment": 94, "reviewStatus": "Pending", "role": "LEAD", "sprint": "Sprint 12"},
        {"id": "SB-002", "storyId": "STR-102", "title": "Dashboard Analytics Module", "assignee": "Divya Menon", "points": 8, "priority": "High", "status": "In Review", "risk": "Medium", "alignment": 88, "reviewStatus": "Approved", "role": "LEAD", "sprint": "Sprint 12"},
        {"id": "SB-003", "storyId": "STR-103", "title": "Email Notification Service", "assignee": "Arjun Patel", "points": 3, "priority": "Medium", "status": "To Do", "risk": "Low", "alignment": 100, "reviewStatus": "—", "role": "LEAD", "sprint": "Sprint 12"},
        {"id": "SB-004", "storyId": "STR-104", "title": "Fix Payment Gateway Timeout", "assignee": "Vikram Singh", "points": 5, "priority": "Critical", "status": "In Progress", "risk": "High", "alignment": 72, "reviewStatus": "Pending", "role": "DEVELOPER", "sprint": "Sprint 12"},
        {"id": "SB-005", "storyId": "STR-105", "title": "CI Pipeline Optimization", "assignee": "Ananya Reddy", "points": 3, "priority": "Medium", "status": "Done", "risk": "Low", "alignment": 96, "reviewStatus": "Approved", "role": "DEVELOPER", "sprint": "Sprint 12"},
    ]
    await db.sprint_boards.insert_many(sprint_boards)
    print(f"✅  Seeded {len(sprint_boards)} sprint board cards")

    # ── Workload Items ──
    workload_items = [
        {"id": "WL-001", "name": "Vikram Singh", "role": "Developer", "taskCount": 8, "storyPoints": 24, "capacity": 72, "status": "Balanced", "sprint": "Sprint 12", "team": "Engineering"},
        {"id": "WL-002", "name": "Sneha Iyer", "role": "Scrum Master", "taskCount": 5, "storyPoints": 18, "capacity": 65, "status": "Balanced", "sprint": "Sprint 12", "team": "Engineering"},
        {"id": "WL-003", "name": "Ananya Reddy", "role": "DevOps", "taskCount": 10, "storyPoints": 30, "capacity": 95, "status": "Overloaded", "sprint": "Sprint 12", "team": "Infrastructure"},
        {"id": "WL-004", "name": "Divya Menon", "role": "QA", "taskCount": 6, "storyPoints": 16, "capacity": 58, "status": "Under", "sprint": "Sprint 12", "team": "Quality Assurance"},
        {"id": "CAP-001", "type": "capacityChart", "week": "Week 1", "capacity": 80, "utilized": 72, "sprint": "Sprint 12"},
        {"id": "CAP-002", "type": "capacityChart", "week": "Week 2", "capacity": 80, "utilized": 85, "sprint": "Sprint 12"},
        {"id": "CAP-003", "type": "capacityChart", "week": "Week 3", "capacity": 80, "utilized": 78, "sprint": "Sprint 12"},
    ]
    await db.workload_items.insert_many(workload_items)
    print(f"✅  Seeded {len(workload_items)} workload items")

    # ── Alignment Items ──
    alignment_items = [
        {"id": "ALN-CEO-001", "type": "company", "category": "Product", "score": 91, "delta": 3, "sprint": "Sprint 12", "role": "CEO"},
        {"id": "ALN-CEO-002", "type": "project", "project": "Sprint Alpha", "score": 88, "delta": -2, "sprint": "Sprint 12", "role": "CEO"},
        {"id": "ALN-PM-001", "type": "member", "member": "Vikram Singh", "score": 94, "delta": 2, "sprint": "Sprint 12", "role": "PM"},
        {"id": "ALN-PM-002", "type": "member", "member": "Sneha Iyer", "score": 87, "delta": 1, "sprint": "Sprint 12", "role": "PM"},
        {"id": "ALN-LEAD-001", "type": "story", "storyId": "STR-102", "title": "Dashboard Analytics Module", "score": 72, "drift": 28, "sprint": "Sprint 12", "role": "LEAD"},
        {"id": "ALN-DEV-001", "type": "devAI", "category": "Architecture Patterns", "score": 88, "sprint": "Sprint 12", "role": "DEVELOPER"},
        {"id": "ALN-DEV-002", "type": "devAI", "category": "Code Style", "score": 95, "sprint": "Sprint 12", "role": "DEVELOPER"},
        {"id": "ALN-TREND-001", "type": "trend", "sprint": "S9", "score": 78, "sprint_num": 9},
        {"id": "ALN-TREND-002", "type": "trend", "sprint": "S10", "score": 80, "sprint_num": 10},
        {"id": "ALN-TREND-003", "type": "trend", "sprint": "S11", "score": 84, "sprint_num": 11},
        {"id": "ALN-TREND-004", "type": "trend", "sprint": "S12", "score": 88, "sprint_num": 12},
    ]
    await db.alignment_items.insert_many(alignment_items)
    print(f"✅  Seeded {len(alignment_items)} alignment items")

    # ── Pull Requests ──
    pull_requests = [
        {"id": "PR-001", "title": "feat: OAuth2 login integration", "author": "Vikram Singh", "branch": "feature/oauth2-login", "base": "develop", "status": "Open", "reviewStatus": "Pending", "comments": 3, "changedFiles": 12, "additions": 340, "deletions": 28, "createdAt": "2 days ago", "sprint": "Sprint 12"},
        {"id": "PR-002", "title": "fix: payment gateway timeout on retry", "author": "Vikram Singh", "branch": "fix/payment-timeout", "base": "develop", "status": "Open", "reviewStatus": "Changes Requested", "comments": 7, "changedFiles": 4, "additions": 56, "deletions": 22, "createdAt": "1 day ago", "sprint": "Sprint 12"},
        {"id": "PR-003", "title": "refactor: dashboard analytics module", "author": "Arjun Patel", "branch": "refactor/dashboard-analytics", "base": "develop", "status": "Merged", "reviewStatus": "Approved", "comments": 2, "changedFiles": 18, "additions": 520, "deletions": 115, "createdAt": "3 days ago", "sprint": "Sprint 12"},
        {"id": "PR-004", "title": "chore: update CI pipeline base image", "author": "Ananya Reddy", "branch": "chore/ci-base-image", "base": "main", "status": "Merged", "reviewStatus": "Approved", "comments": 1, "changedFiles": 2, "additions": 8, "deletions": 8, "createdAt": "4 days ago", "sprint": "Sprint 12"},
        {"id": "PR-005", "title": "feat: email notification service", "author": "Arjun Patel", "branch": "feature/email-notifications", "base": "develop", "status": "Draft", "reviewStatus": "Draft", "comments": 0, "changedFiles": 9, "additions": 210, "deletions": 0, "createdAt": "Today", "sprint": "Sprint 12"},
    ]
    await db.pull_requests.insert_many(pull_requests)
    print(f"✅  Seeded {len(pull_requests)} pull requests")

    # ── Branches ──
    branches = [
        {"id": "BR-001", "name": "feature/oauth2-login", "author": "Vikram Singh", "status": "Active", "lastCommit": "2h ago", "commits": 14, "aheadBy": 14, "behindBy": 2, "ciStatus": "Passed", "sprint": "Sprint 12"},
        {"id": "BR-002", "name": "fix/payment-timeout", "author": "Vikram Singh", "status": "Active", "lastCommit": "5h ago", "commits": 5, "aheadBy": 5, "behindBy": 0, "ciStatus": "Failed", "sprint": "Sprint 12"},
        {"id": "BR-003", "name": "feature/email-notifications", "author": "Arjun Patel", "status": "Draft", "lastCommit": "1d ago", "commits": 8, "aheadBy": 8, "behindBy": 3, "ciStatus": "Running", "sprint": "Sprint 12"},
    ]
    await db.branches.insert_many(branches)
    print(f"✅  Seeded {len(branches)} branches")

    # ── Submissions ──
    submissions = [
        {"id": "SUB-001", "storyId": "STR-101", "title": "OAuth2 Login Feature", "submittedBy": "Vikram Singh", "submittedAt": "2026-02-19", "status": "Under Review", "reviewedBy": "Sneha Iyer", "tab": "pending", "aiScore": 88, "comments": "Implementation looks solid. Minor security concern on token storage."},
        {"id": "SUB-002", "storyId": "STR-103", "title": "Email Notification Service", "submittedBy": "Arjun Patel", "submittedAt": "2026-02-18", "status": "Approved", "reviewedBy": "Sneha Iyer", "tab": "approved", "aiScore": 95, "comments": "Excellent implementation. Well tested."},
        {"id": "SUB-003", "storyId": "STR-104", "title": "Payment Gateway Timeout Fix", "submittedBy": "Vikram Singh", "submittedAt": "2026-02-17", "status": "Rejected", "reviewedBy": "Sneha Iyer", "tab": "rejected", "aiScore": 62, "comments": "Missing error handling for network retries. Please revise."},
    ]
    await db.submissions.insert_many(submissions)
    print(f"✅  Seeded {len(submissions)} submissions")

    # ── Progress Snapshots ──
    progress_snapshots = [
        {"id": "PS-DEV-001", "type": "sprintContribution", "sprint": "S7", "sp": 18, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-DEV-002", "type": "sprintContribution", "sprint": "S8", "sp": 22, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-DEV-003", "type": "sprintContribution", "sprint": "S9", "sp": 20, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-DEV-004", "type": "sprintContribution", "sprint": "S10", "sp": 24, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-DEV-005", "type": "sprintContribution", "sprint": "S11", "sp": 21, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-DEV-006", "type": "sprintContribution", "sprint": "S12", "sp": 26, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-ALN-001", "type": "alignmentTrend", "sprint": "S7", "score": 80, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-ALN-002", "type": "alignmentTrend", "sprint": "S8", "score": 83, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-ALN-003", "type": "alignmentTrend", "sprint": "S9", "score": 86, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-ALN-004", "type": "alignmentTrend", "sprint": "S10", "score": 88, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-ALN-005", "type": "alignmentTrend", "sprint": "S11", "score": 90, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-ALN-006", "type": "alignmentTrend", "sprint": "S12", "score": 94, "role": "DEVELOPER", "member": "Vikram Singh"},
        {"id": "PS-BEH-001", "type": "behaviourSnapshot", "member": "Vikram Singh", "communication": 9, "ownership": 9, "teamwork": 8, "leadership": 7, "discipline": 9, "sprint": "Sprint 12"},
    ]
    await db.progress_snapshots.insert_many(progress_snapshots)
    print(f"✅  Seeded {len(progress_snapshots)} progress snapshots")

    # ── DevOps Tasks ──
    devops_tasks = [
        {"id": "OPS-001", "title": "Upgrade K8s to 1.29", "type": "Infra", "assignee": "Ananya Reddy", "status": "In Progress", "priority": "High", "ciAlign": True, "sprint": "Sprint 12", "dueDate": "Feb 25, 2026", "aiVerified": False},
        {"id": "OPS-002", "title": "Rotate SSL Certificates", "type": "Security", "assignee": "Ananya Reddy", "status": "Done", "priority": "Critical", "ciAlign": True, "sprint": "Sprint 12", "dueDate": "Feb 20, 2026", "aiVerified": True},
        {"id": "OPS-003", "title": "Set up Prometheus alerting", "type": "Monitoring", "assignee": "Ananya Reddy", "status": "To Do", "priority": "Medium", "ciAlign": False, "sprint": "Sprint 12", "dueDate": "Mar 1, 2026", "aiVerified": False},
        {"id": "OPS-004", "title": "Update Terraform modules", "type": "Infra", "assignee": "Ananya Reddy", "status": "In Progress", "priority": "High", "ciAlign": True, "sprint": "Sprint 12", "dueDate": "Feb 28, 2026", "aiVerified": False},
        {"id": "OPS-005", "title": "Database backup validation", "type": "DB", "assignee": "Ananya Reddy", "status": "Done", "priority": "High", "ciAlign": True, "sprint": "Sprint 12", "dueDate": "Feb 18, 2026", "aiVerified": True},
    ]
    await db.devops_tasks.insert_many(devops_tasks)
    print(f"✅  Seeded {len(devops_tasks)} DevOps tasks")

    # ── Incidents ──
    incidents = [
        {
            "id": "INC-001", "title": "API Gateway 502 Cascade", "severity": "Critical", "status": "Resolved",
            "affectedService": "API Gateway", "startTime": "Feb 18, 2026 02:14", "resolvedAt": "Feb 18, 2026 03:41",
            "duration": "1h 27m", "rootCause": "Upstream service memory leak caused cascading 502s.",
            "aiSummary": "Memory pressure on Node B triggered connection pool exhaustion. Fix: horizontal scale + memory limits enforced.",
            "assignee": "Ananya Reddy", "sprint": "Sprint 12",
        },
        {
            "id": "INC-002", "title": "DB Replication Lag Spike", "severity": "High", "status": "Resolved",
            "affectedService": "MongoDB Replica Set", "startTime": "Feb 16, 2026 14:30", "resolvedAt": "Feb 16, 2026 16:00",
            "duration": "1h 30m", "rootCause": "High write throughput during data migration exceeded replica capacity.",
            "aiSummary": "Migration script batching was too aggressive. Reduced batch size and added write delay.",
            "assignee": "Ananya Reddy", "sprint": "Sprint 12",
        },
        {
            "id": "INC-003", "title": "Payment Gateway Timeout", "severity": "Medium", "status": "Monitoring",
            "affectedService": "Payment Service", "startTime": "Feb 20, 2026 10:05", "resolvedAt": None,
            "duration": "Ongoing", "rootCause": "Third-party gateway intermittent latency spike.",
            "aiSummary": "Implement circuit breaker pattern. Currently monitoring P99 latency.",
            "assignee": "Vikram Singh", "sprint": "Sprint 12",
        },
    ]
    await db.incidents.insert_many(incidents)
    print(f"✅  Seeded {len(incidents)} incidents")

    # ── Infrastructure Changes ──
    infrastructure_changes = [
        {"id": "CHG-001", "title": "K8s Base Image Update", "type": "Docker", "risk": "Low", "status": "Deployed", "author": "Ananya Reddy", "date": "Feb 20, 2026", "description": "Updated base image to node:20-alpine for security patches.", "sprint": "Sprint 12"},
        {"id": "CHG-002", "title": "DB Connection Pool Resize", "type": "Database", "risk": "Medium", "status": "Staged", "author": "Ananya Reddy", "date": "Feb 19, 2026", "description": "Increased MongoDB connection pool from 50 to 100.", "sprint": "Sprint 12"},
        {"id": "CHG-003", "title": "Terraform: Add Auto-Scaling Group", "type": "Terraform", "risk": "High", "status": "Pending Approval", "author": "Ananya Reddy", "date": "Feb 21, 2026", "description": "New ASG for API Gateway with min=2, max=8 instances.", "sprint": "Sprint 12"},
        {"id": "CHG-004", "title": "SSL Certificate Renewal", "type": "Security", "risk": "Low", "status": "Deployed", "author": "Ananya Reddy", "date": "Feb 18, 2026", "description": "Renewed wildcard SSL cert for *.exactiomark.com.", "sprint": "Sprint 12"},
    ]
    await db.infrastructure_changes.insert_many(infrastructure_changes)
    print(f"✅  Seeded {len(infrastructure_changes)} infrastructure changes")

    # ── Logs & Alerts ──
    logs_alerts = [
        {"id": "LOG-001", "timestamp": "Feb 20 14:32:11", "level": "ERROR", "category": "API Gateway", "message": "Connection pool exhausted — retrying in 200ms", "source": "api-gateway-pod-3", "count": 47, "sprint": "Sprint 12"},
        {"id": "LOG-002", "timestamp": "Feb 20 13:15:02", "level": "WARN", "category": "Auth Service", "message": "JWT token near expiry not refreshed (Safari agent)", "source": "auth-service-pod-1", "count": 12, "sprint": "Sprint 12"},
        {"id": "LOG-003", "timestamp": "Feb 20 11:05:44", "level": "INFO", "category": "Deployment", "message": "v2.4.1-rc3 deployed to staging successfully", "source": "ci-runner-7", "count": 1, "sprint": "Sprint 12"},
        {"id": "LOG-004", "timestamp": "Feb 20 09:48:22", "level": "CRITICAL", "category": "Database", "message": "Replication lag exceeded 30s threshold on replica-2", "source": "mongo-replica-2", "count": 1, "sprint": "Sprint 12"},
        {"id": "LOG-005", "timestamp": "Feb 19 22:10:55", "level": "WARN", "category": "Payment Service", "message": "Stripe API P95 latency: 850ms (threshold: 500ms)", "source": "payment-svc-pod-2", "count": 23, "sprint": "Sprint 12"},
    ]
    await db.logs_alerts.insert_many(logs_alerts)
    print(f"✅  Seeded {len(logs_alerts)} logs/alerts")

    # ── Test Cases ──
    test_cases = [
        {"id": "TC-001", "title": "Login with valid credentials", "story": "STR-101", "type": "Functional", "priority": "High", "status": "Passed", "assignee": "Divya Menon", "sprint": "Sprint 12", "steps": ["Open login page", "Enter valid email and password", "Click Login", "Assert dashboard renders"], "expected": "User redirected to role dashboard"},
        {"id": "TC-002", "title": "Login with invalid password", "story": "STR-101", "type": "Functional", "priority": "High", "status": "Passed", "assignee": "Divya Menon", "sprint": "Sprint 12", "steps": ["Open login page", "Enter valid email but wrong password", "Click Login", "Assert error toast shown"], "expected": "Error: Invalid credentials shown"},
        {"id": "TC-003", "title": "Payment gateway timeout handling", "story": "STR-104", "type": "Integration", "priority": "Critical", "status": "Failed", "assignee": "Divya Menon", "sprint": "Sprint 12", "steps": ["Trigger payment with mock slow gateway", "Wait for timeout", "Assert retry logic fires", "Assert graceful error returned"], "expected": "Retry 3x then return 504 with friendly message"},
        {"id": "TC-004", "title": "Dashboard analytics loads within 2s", "story": "STR-102", "type": "Performance", "priority": "Medium", "status": "Passed", "assignee": "Divya Menon", "sprint": "Sprint 12", "steps": ["Load dashboard page", "Measure time to interactive"], "expected": "LCP < 2000ms"},
        {"id": "TC-005", "title": "Email notification sent on story assignment", "story": "STR-103", "type": "Functional", "priority": "Medium", "status": "Pending", "assignee": "Divya Menon", "sprint": "Sprint 12", "steps": ["Assign story to Vikram", "Check email inbox"], "expected": "Email received within 30s"},
        {"id": "TC-006", "title": "OAuth2 token refresh on expiry", "story": "STR-101", "type": "Security", "priority": "High", "status": "Failed", "assignee": "Divya Menon", "sprint": "Sprint 12", "steps": ["Login via OAuth2", "Wait for token expiry", "Make API call", "Assert 200 returned (not 401)"], "expected": "Token silently refreshed"},
    ]
    await db.test_cases.insert_many(test_cases)
    print(f"✅  Seeded {len(test_cases)} test cases")

    # ── Test Runs ──
    test_runs = [
        {"id": 1, "build": "v2.4.1-rc3", "env": "Staging", "total": 86, "passed": 78, "failed": 8, "duration": "12m 34s", "ciStatus": "Passed", "coverage": 82, "sprint": "Sprint 12"},
        {"id": 2, "build": "v3.1.0-rc1", "env": "Staging", "total": 42, "passed": 36, "failed": 6, "duration": "8m 12s", "ciStatus": "Failed", "coverage": 78, "sprint": "Sprint 12"},
        {"id": 3, "build": "v2.3.8-hotfix", "env": "Dev", "total": 24, "passed": 20, "failed": 4, "duration": "4m 48s", "ciStatus": "Passed", "coverage": 65, "sprint": "Sprint 12"},
        {"id": 4, "build": "v1.5.0-beta", "env": "Dev", "total": 18, "passed": 16, "failed": 2, "duration": "3m 22s", "ciStatus": "Passed", "coverage": 88, "sprint": "Sprint 12"},
        {"id": 5, "build": "v2.4.0-rc2", "env": "Staging", "total": 86, "passed": 82, "failed": 4, "duration": "11m 56s", "ciStatus": "Passed", "coverage": 85, "sprint": "Sprint 12"},
        {"id": 6, "build": "v1.0.0-alpha", "env": "Dev", "total": 15, "passed": 12, "failed": 3, "duration": "2m 45s", "ciStatus": "Failed", "coverage": 55, "sprint": "Sprint 12"},
    ]
    await db.test_runs.insert_many(test_runs)
    print(f"✅  Seeded {len(test_runs)} test runs")

    # ── Regression Suites ──
    regression_suites = [
        {"id": "REG-001", "module": "Authentication", "total": 24, "passed": 22, "failed": 2, "status": "Partial", "sprint": "Sprint 12", "lastRun": "Feb 20, 2026"},
        {"id": "REG-002", "module": "Payment Gateway", "total": 18, "passed": 14, "failed": 4, "status": "Failing", "sprint": "Sprint 12", "lastRun": "Feb 20, 2026"},
        {"id": "REG-003", "module": "Dashboard Analytics", "total": 12, "passed": 12, "failed": 0, "status": "Passing", "sprint": "Sprint 12", "lastRun": "Feb 19, 2026"},
        {"id": "REG-004", "module": "Email Notifications", "total": 8, "passed": 8, "failed": 0, "status": "Passing", "sprint": "Sprint 12", "lastRun": "Feb 19, 2026"},
        {"id": "REG-005", "module": "Sprint Board API", "total": 16, "passed": 15, "failed": 1, "status": "Partial", "sprint": "Sprint 12", "lastRun": "Feb 20, 2026"},
    ]
    await db.regression_suites.insert_many(regression_suites)
    print(f"✅  Seeded {len(regression_suites)} regression suites")

    # ── Release Checks ──
    release_checks = [
        {"id": "RC-001", "category": "Test Coverage", "check": "Unit test coverage >= 80%", "status": "Pass", "value": "82%", "sprint": "Sprint 12", "blocking": True},
        {"id": "RC-002", "category": "Test Coverage", "check": "Integration tests passing", "status": "Fail", "value": "94% (4 failing)", "sprint": "Sprint 12", "blocking": True},
        {"id": "RC-003", "category": "Security", "check": "No critical security vulnerabilities", "status": "Pass", "value": "0 critical", "sprint": "Sprint 12", "blocking": True},
        {"id": "RC-004", "category": "Performance", "check": "API P95 latency < 500ms", "status": "Warn", "value": "P95: 620ms", "sprint": "Sprint 12", "blocking": False},
        {"id": "RC-005", "category": "Deployment", "check": "Staging deployment successful", "status": "Pass", "value": "v2.4.1-rc3", "sprint": "Sprint 12", "blocking": True},
        {"id": "RC-006", "category": "Documentation", "check": "API docs up to date", "status": "Warn", "value": "2 endpoints undocumented", "sprint": "Sprint 12", "blocking": False},
    ]
    await db.release_checks.insert_many(release_checks)
    print(f"✅  Seeded {len(release_checks)} release checks")

    # ── Behaviour Reviews ──
    behaviour_reviews = [
        {"id": "BHR-001", "member": "Vikram Singh", "ratedBy": "Priya Sharma", "month": "Feb 2026", "sprint": "Sprint 12", "communication": 9, "ownership": 9, "teamwork": 8, "leadership": 7, "discipline": 9, "overall": 8.4, "comment": "Outstanding sprint. Delivered 26 SP with zero regressions."},
        {"id": "BHR-002", "member": "Sneha Iyer", "ratedBy": "Priya Sharma", "month": "Feb 2026", "sprint": "Sprint 12", "communication": 9, "ownership": 8, "teamwork": 9, "leadership": 8, "discipline": 9, "overall": 8.6, "comment": "Excellent facilitation. Velocity improved by 12%."},
        {"id": "BHR-003", "member": "Ananya Reddy", "ratedBy": "Priya Sharma", "month": "Feb 2026", "sprint": "Sprint 12", "communication": 8, "ownership": 9, "teamwork": 8, "leadership": 8, "discipline": 9, "overall": 8.4, "comment": "Zero downtime incidents this sprint. Proactive on infra risks."},
        {"id": "BHR-004", "member": "Divya Menon", "ratedBy": "Priya Sharma", "month": "Feb 2026", "sprint": "Sprint 12", "communication": 8, "ownership": 8, "teamwork": 9, "leadership": 6, "discipline": 8, "overall": 7.8, "comment": "Good QA coverage. Can improve on blocker escalation speed."},
        {"id": "BHR-005", "member": "Arjun Patel", "ratedBy": "Priya Sharma", "month": "Feb 2026", "sprint": "Sprint 12", "communication": 9, "ownership": 8, "teamwork": 8, "leadership": 8, "discipline": 8, "overall": 8.2, "comment": "Strong alignment scores. Stakeholder management is excellent."},
    ]
    await db.behaviour_reviews.insert_many(behaviour_reviews)
    print(f"✅  Seeded {len(behaviour_reviews)} behaviour reviews")

    # ── Company Settings ──
    company_settings = [
        {
            "id": "settings-001",
            "companyName": "Exactiomark Technologies",
            "sprintDurationWeeks": 2,
            "velocityTarget": 80,
            "performanceWeights": {
                "alignment": 30, "onTime": 25, "behaviour": 25, "rejection": 20
            },
            "thresholds": {
                "promotionMinScore": 85, "riskFlagBehaviour": 6, "riskFlagAlignment": 70
            },
            "sprintPolicy": {
                "maxStoriesPerDev": 6, "reviewSLADays": 1, "standupTimebox": 15
            },
            "accessControl": {
                "hrCanSeeScores": True, "ceoCanSeeAll": True, "developerSeeOwnOnly": True
            },
        }
    ]
    await db.company_settings.insert_many(company_settings)
    print(f"✅  Seeded company settings")

    # ── Page Metrics (chart/trend data for dashboards) ──
    page_metrics = [
        {"id": "PM-EXEC-S10", "type": "executionData", "sprint": "S10", "planned": 78, "delivered": 72, "velocity": 68, "role": "CEO"},
        {"id": "PM-EXEC-S11", "type": "executionData", "sprint": "S11", "planned": 82, "delivered": 80, "velocity": 74, "role": "CEO"},
        {"id": "PM-EXEC-S12", "type": "executionData", "sprint": "S12", "planned": 85, "delivered": 83, "velocity": 80, "role": "CEO"},
        {"id": "PM-QA-S10", "type": "sprintQuality", "sprint": "S10", "bugs": 8, "passed": 74, "coverage": 78, "role": "QA"},
        {"id": "PM-QA-S11", "type": "sprintQuality", "sprint": "S11", "bugs": 5, "passed": 80, "coverage": 80, "role": "QA"},
        {"id": "PM-QA-S12", "type": "sprintQuality", "sprint": "S12", "bugs": 8, "passed": 78, "coverage": 82, "role": "QA"},
        {"id": "PM-DEP-S10", "type": "deployFrequency", "sprint": "S10", "count": 4, "role": "DEVOPS"},
        {"id": "PM-DEP-S11", "type": "deployFrequency", "sprint": "S11", "count": 6, "role": "DEVOPS"},
        {"id": "PM-DEP-S12", "type": "deployFrequency", "sprint": "S12", "count": 5, "role": "DEVOPS"},
    ]
    await db.page_metrics.insert_many(page_metrics)
    print(f"✅  Seeded {len(page_metrics)} page metrics")

    print("\n==== PHASE 2: Role-Specific Page Collections ====\n")

    # ═══════════════════════════════════════════════════════════════
    # USER LOGINS — employee_id, org_password, user_password
    # ═══════════════════════════════════════════════════════════════
    user_logins = [
        {"id": "UL-001", "employee_id": "EMP-CEO-001", "name": "Rajesh Mehta", "email": "rajesh@exactiomark.com", "role": "CEO", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
        {"id": "UL-002", "employee_id": "EMP-HR-001", "name": "Priya Sharma", "email": "priya@exactiomark.com", "role": "HR", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
        {"id": "UL-003", "employee_id": "EMP-PM-001", "name": "Arjun Patel", "email": "arjun@exactiomark.com", "role": "PM", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
        {"id": "UL-004", "employee_id": "EMP-LEAD-001", "name": "Sneha Iyer", "email": "sneha@exactiomark.com", "role": "LEAD", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
        {"id": "UL-005", "employee_id": "EMP-DEV-001", "name": "Vikram Singh", "email": "vikram@exactiomark.com", "role": "DEVELOPER", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
        {"id": "UL-006", "employee_id": "EMP-OPS-001", "name": "Ananya Reddy", "email": "ananya@exactiomark.com", "role": "DEVOPS", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
        {"id": "UL-007", "employee_id": "EMP-QA-001", "name": "Divya Menon", "email": "divya@exactiomark.com", "role": "QA", "org_password": "$2b$12$orgHashPlaceholder", "user_password": "$2b$12$userHashPlaceholder", "created_at": "2025-01-01", "is_active": True},
    ]
    await db.user_logins.insert_many(user_logins)
    print(f"✅  Seeded {len(user_logins)} user logins")

    # ═══════════════════════════════════════════════════════════════
    # CEO — Execution Data (CEODashboard.jsx)
    # ═══════════════════════════════════════════════════════════════
    execution_weeks = [
        {"id": "ew-1", "week": "W1", "health": 78, "target": 85},
        {"id": "ew-2", "week": "W2", "health": 82, "target": 85},
        {"id": "ew-3", "week": "W3", "health": 76, "target": 85},
        {"id": "ew-4", "week": "W4", "health": 89, "target": 85},
        {"id": "ew-5", "week": "W5", "health": 91, "target": 85},
        {"id": "ew-6", "week": "W6", "health": 85, "target": 85},
        {"id": "ew-7", "week": "W7", "health": 93, "target": 85},
        {"id": "ew-8", "week": "W8", "health": 88, "target": 85},
    ]
    await db.execution_weeks.insert_many(execution_weeks)
    print(f"✅  Seeded {len(execution_weeks)} execution weeks")

    sprint_status_slices = [
        {"id": "ss-1", "name": "On Track", "value": 12, "color": "#10b981"},
        {"id": "ss-2", "name": "At Risk", "value": 4, "color": "#f59e0b"},
        {"id": "ss-3", "name": "Delayed", "value": 2, "color": "#ef4444"},
        {"id": "ss-4", "name": "Completed", "value": 8, "color": "#3b82f6"},
    ]
    await db.sprint_status_slices.insert_many(sprint_status_slices)
    print(f"✅  Seeded {len(sprint_status_slices)} sprint status slices")

    ceo_escalations = [
        {"id": 1, "title": "Backend API latency spike", "severity": "High", "project": "Sprint Alpha", "time": "2 hours ago", "status": "Open"},
        {"id": 2, "title": "Client deliverable deadline at risk", "severity": "Critical", "project": "Sprint Beta", "time": "5 hours ago", "status": "Escalated"},
        {"id": 3, "title": "Resource conflict between teams", "severity": "Medium", "project": "Sprint Gamma", "time": "1 day ago", "status": "Resolved"},
        {"id": 4, "title": "Security vulnerability in auth module", "severity": "Critical", "project": "Sprint Alpha", "time": "1 day ago", "status": "In Progress"},
    ]
    await db.ceo_escalations.insert_many(ceo_escalations)
    print(f"✅  Seeded {len(ceo_escalations)} CEO escalations")

    # CEO — Execution Health (ExecutionHealth.jsx)
    health_factors = [
        {"id": "hf-1", "name": "Completion Rate", "weight": 25, "score": 91, "color": "#10b981"},
        {"id": "hf-2", "name": "Alignment Accuracy", "weight": 25, "score": 87, "color": "#3b82f6"},
        {"id": "hf-3", "name": "Approval Speed", "weight": 15, "score": 78, "color": "#f59e0b"},
        {"id": "hf-4", "name": "CI Stability", "weight": 15, "score": 95, "color": "#8b5cf6"},
        {"id": "hf-5", "name": "Workload Balance", "weight": 10, "score": 72, "color": "#ec4899"},
        {"id": "hf-6", "name": "Escalations", "weight": 10, "score": 85, "color": "#ef4444"},
    ]
    await db.health_factors.insert_many(health_factors)
    print(f"✅  Seeded {len(health_factors)} health factors")

    story_risks = [
        {"id": "US-104", "title": "SSO provider config", "developer": "Ananya R.", "risk": 82, "reason": "External dependency delay"},
        {"id": "US-109", "title": "CI/CD pipeline staging", "developer": "Ananya R.", "risk": 68, "reason": "Infrastructure provisioning pending"},
        {"id": "US-106", "title": "MFA setup wizard", "developer": "Sneha I.", "risk": 55, "reason": "Design spec incomplete"},
        {"id": "US-105", "title": "Password policy enforcement", "developer": "Vikram S.", "risk": 35, "reason": "Minor scope clarification needed"},
        {"id": "US-103", "title": "Role permission matrix", "developer": "Vikram S.", "risk": 22, "reason": "In review – awaiting approval"},
    ]
    await db.story_risks.insert_many(story_risks)
    print(f"✅  Seeded {len(story_risks)} story risks")

    dev_risk_contributions = [
        {"id": "drc-1", "name": "Ananya R.", "riskScore": 75, "storiesAtRisk": 2, "avgDelay": "1.8 days"},
        {"id": "drc-2", "name": "Sneha I.", "riskScore": 42, "storiesAtRisk": 1, "avgDelay": "0.5 days"},
        {"id": "drc-3", "name": "Vikram S.", "riskScore": 28, "storiesAtRisk": 1, "avgDelay": "0.2 days"},
    ]
    await db.dev_risk_contributions.insert_many(dev_risk_contributions)
    print(f"✅  Seeded {len(dev_risk_contributions)} dev risk contributions")

    # CEO — Risk Escalations (RiskEscalations.jsx)
    active_risks = [
        {"id": "ar-1", "storyId": "US-104", "riskType": "Delay", "riskLevel": "High", "responsible": "Ananya R.", "desc": "SSO provider API not responding"},
        {"id": "ar-2", "storyId": "US-109", "riskType": "DevOps Failure", "riskLevel": "Critical", "responsible": "Ananya R.", "desc": "Staging infra not provisioned"},
        {"id": "ar-3", "storyId": "US-106", "riskType": "Scope Drift", "riskLevel": "Medium", "responsible": "Sneha I.", "desc": "MFA design spec changed mid-sprint"},
        {"id": "ar-4", "storyId": "US-110", "riskType": "Delay", "riskLevel": "Low", "responsible": "Sneha I.", "desc": "Test suite blocked on US-109 completion"},
    ]
    await db.active_risks.insert_many(active_risks)
    print(f"✅  Seeded {len(active_risks)} active risks")

    escalation_events = [
        {"id": 1, "time": "Feb 18, 10:32 AM", "event": "Escalation triggered", "detail": "CI/CD pipeline staging build failures exceeded threshold", "notified": "Arjun Patel (PM)", "resolution": "Pending", "severity": "Critical"},
        {"id": 2, "time": "Feb 17, 3:15 PM", "event": "Escalation triggered", "detail": "SSO provider config blocked for 48+ hours", "notified": "Rajesh Mehta (CEO)", "resolution": "6 hrs", "severity": "High"},
        {"id": 3, "time": "Feb 15, 11:00 AM", "event": "Escalation triggered", "detail": "Review bottleneck – 3 PRs pending > 24h", "notified": "Sneha Iyer (Lead)", "resolution": "2 hrs", "severity": "Medium"},
        {"id": 4, "time": "Feb 14, 9:45 AM", "event": "Escalation resolved", "detail": "Backend API latency spike – fixed by scaling", "notified": "Arjun Patel (PM)", "resolution": "4 hrs", "severity": "High"},
    ]
    await db.escalation_events.insert_many(escalation_events)
    print(f"✅  Seeded {len(escalation_events)} escalation events")

    risk_patterns = [
        {"id": "rp-1", "title": "Repeated Backend Delay", "occurrences": 4, "sprints": "Last 3 sprints", "impact": "Avg 1.5 day delay per sprint", "recommendation": "Consider dedicated backend DevOps support or pre-provisioned staging environments.", "color": "#ef4444"},
        {"id": "rp-2", "title": "Review Bottleneck Detection", "occurrences": 6, "sprints": "Last 4 sprints", "impact": "Avg 18 hrs approval delay", "recommendation": "Introduce auto-assign reviewers and set SLA of 4 hrs for code reviews.", "color": "#f59e0b"},
        {"id": "rp-3", "title": "Scope Drift in Design Stories", "occurrences": 3, "sprints": "Last 2 sprints", "impact": "12% spillover increase", "recommendation": "Lock acceptance criteria before sprint start. Add design review checkpoint.", "color": "#8b5cf6"},
    ]
    await db.risk_patterns.insert_many(risk_patterns)
    print(f"✅  Seeded {len(risk_patterns)} risk patterns")

    # CEO — Backlog / Stories (BacklogStories.jsx)
    backlog_stories = [
        {"id": "ST-101", "title": "Implement Auth Module", "desc": "Build the authentication module with JWT-based login, registration, and session management.", "module": "Auth", "type": "Dev", "assignee": "Vikram Singh", "alignment": 94, "status": "Done", "approval": "Approved", "storyPoints": 8, "priority": "Critical", "sprint_id": "sprint-alpha", "risk": "Low", "delay": 0, "est": "3d", "actual": "2.5d"},
        {"id": "ST-102", "title": "Setup CI/CD Pipeline", "desc": "Configure continuous integration and deployment pipeline for staging and production environments.", "module": "DevOps", "type": "DevOps", "assignee": "Ananya Reddy", "alignment": 78, "status": "In Progress", "approval": "Pending Review", "storyPoints": 8, "priority": "High", "sprint_id": "sprint-alpha", "risk": "High", "delay": 2, "est": "4d", "actual": "—"},
        {"id": "ST-103", "title": "User Profile API", "desc": "Create RESTful API endpoints for user profile CRUD operations with validation.", "module": "Users", "type": "Dev", "assignee": "Vikram Singh", "alignment": 88, "status": "In Review", "approval": "Pending Review", "storyPoints": 5, "priority": "Medium", "sprint_id": "sprint-alpha", "risk": "Low", "delay": 0, "est": "2d", "actual": "2d"},
        {"id": "ST-104", "title": "Dashboard UI Redesign", "desc": "Redesign the main dashboard interface with new KPI cards, charts, and responsive layout.", "module": "Frontend", "type": "Dev", "assignee": "Rahul Verma", "alignment": 65, "status": "In Progress", "approval": "Not Started", "storyPoints": 8, "priority": "High", "sprint_id": "sprint-alpha", "risk": "High", "delay": 3, "est": "5d", "actual": "—"},
        {"id": "ST-105", "title": "Integration Tests – Sprint API", "desc": "Write comprehensive integration tests for all sprint-related API endpoints.", "module": "QA", "type": "QA", "assignee": "Meera Nair", "alignment": 85, "status": "Done", "approval": "Approved", "storyPoints": 5, "priority": "Medium", "sprint_id": "sprint-alpha", "risk": "Low", "delay": 0, "est": "2d", "actual": "1.5d"},
        {"id": "ST-106", "title": "Database Migration Script", "desc": "Create migration scripts for schema changes including new indexes and constraints.", "module": "DevOps", "type": "DevOps", "assignee": "Ananya Reddy", "alignment": 72, "status": "In Progress", "approval": "Pending Review", "storyPoints": 5, "priority": "Medium", "sprint_id": "sprint-alpha", "risk": "Medium", "delay": 1, "est": "2d", "actual": "—"},
        {"id": "ST-107", "title": "Notification Service", "desc": "Build real-time notification service with WebSocket support for push notifications.", "module": "Backend", "type": "Dev", "assignee": "Karan Joshi", "alignment": 58, "status": "To Do", "approval": "Not Started", "storyPoints": 8, "priority": "High", "sprint_id": "sprint-alpha", "risk": "High", "delay": 5, "est": "4d", "actual": "—"},
        {"id": "ST-108", "title": "Load Testing Setup", "desc": "Set up load testing infrastructure using k6 with baseline performance benchmarks.", "module": "QA", "type": "QA", "assignee": "Meera Nair", "alignment": 90, "status": "Done", "approval": "Approved", "storyPoints": 5, "priority": "Low", "sprint_id": "sprint-alpha", "risk": "Low", "delay": 0, "est": "1.5d", "actual": "1d"},
        {"id": "ST-109", "title": "API Rate Limiting", "desc": "Implement rate limiting middleware with Redis-based token bucket algorithm.", "module": "Backend", "type": "Dev", "assignee": "Vikram Singh", "alignment": 82, "status": "In Review", "approval": "Pending Review", "storyPoints": 4, "priority": "Medium", "sprint_id": "sprint-alpha", "risk": "Low", "delay": 0, "est": "1.5d", "actual": "1.5d"},
        {"id": "ST-110", "title": "Monitoring Dashboard", "desc": "Create Prometheus-Grafana monitoring dashboard for all microservices health metrics.", "module": "DevOps", "type": "DevOps", "assignee": "Ananya Reddy", "alignment": 70, "status": "To Do", "approval": "Not Started", "storyPoints": 5, "priority": "Medium", "sprint_id": "sprint-alpha", "risk": "Medium", "delay": 0, "est": "3d", "actual": "—"},
    ]
    await db.stories.insert_many(backlog_stories)
    print(f"✅  Seeded {len(backlog_stories)} backlog stories")

    # CEO — Performance Insights (PerformanceInsights.jsx)
    performance_members = [
        {"id": "pm-1", "name": "Vikram Singh", "role": "Developer", "alignment": 91, "onTime": 94, "rejection": 5, "behaviour": 8.5, "sprintContrib": 95, "overall": 89.2, "promotion": True},
        {"id": "pm-2", "name": "Sneha Iyer", "role": "Scrum Master", "alignment": 87, "onTime": 88, "rejection": 8, "behaviour": 9.0, "sprintContrib": 85, "overall": 86.8, "promotion": True},
        {"id": "pm-3", "name": "Ananya Reddy", "role": "DevOps", "alignment": 78, "onTime": 72, "rejection": 15, "behaviour": 7.5, "sprintContrib": 75, "overall": 74.3, "promotion": False},
        {"id": "pm-4", "name": "Arjun Patel", "role": "Sprint Master", "alignment": 85, "onTime": 90, "rejection": 6, "behaviour": 8.8, "sprintContrib": 88, "overall": 85.5, "promotion": True},
        {"id": "pm-5", "name": "Priya Sharma", "role": "HR", "alignment": 82, "onTime": 95, "rejection": 3, "behaviour": 9.2, "sprintContrib": 82, "overall": 88.1, "promotion": True},
    ]
    await db.performance_members.insert_many(performance_members)
    print(f"✅  Seeded {len(performance_members)} performance members")

    # CEO — Sprint Retrospective (SprintRetrospective.jsx)
    ceo_improvements = [
        {"id": "ci-1", "action": "Pre-provision staging environments before sprint start", "assignee": "Ananya R.", "deadline": "Sprint Beta", "priority": "High"},
        {"id": "ci-2", "action": "Lock acceptance criteria 2 days before sprint planning", "assignee": "Arjun Patel", "deadline": "Next Sprint", "priority": "Medium"},
        {"id": "ci-3", "action": "Add auto-assign for code reviews with 4h SLA", "assignee": "Sneha I.", "deadline": "Sprint Beta", "priority": "High"},
        {"id": "ci-4", "action": "Weekly workload rebalancing check-in", "assignee": "Arjun Patel", "deadline": "Ongoing", "priority": "Medium"},
    ]
    await db.ceo_improvements.insert_many(ceo_improvements)
    print(f"✅  Seeded {len(ceo_improvements)} CEO improvements")

    ceo_behaviour_feedback = [
        {"id": "cbf-1", "name": "Vikram Singh", "communication": 9, "ownership": 9, "teamwork": 8, "adaptability": 8, "notes": "Consistently delivers high-quality code. Excellent problem solver."},
        {"id": "cbf-2", "name": "Sneha Iyer", "communication": 9, "ownership": 8, "teamwork": 9, "adaptability": 9, "notes": "Great facilitator. Improved review throughput significantly."},
        {"id": "cbf-3", "name": "Ananya Reddy", "communication": 7, "ownership": 8, "teamwork": 7, "adaptability": 7, "notes": "Technically strong but workload management needs support."},
    ]
    await db.ceo_behaviour_feedback.insert_many(ceo_behaviour_feedback)
    print(f"✅  Seeded {len(ceo_behaviour_feedback)} CEO behaviour feedback entries")

    # ═══════════════════════════════════════════════════════════════
    # PM — PMWorkload.jsx
    # ═══════════════════════════════════════════════════════════════
    pm_workload = [
        {"id": "pw-1", "name": "Vikram Singh", "assigned": 8, "completed": 6, "pending": 1, "overdue": 1, "capacity": 72},
        {"id": "pw-2", "name": "Sneha Iyer", "assigned": 5, "completed": 4, "pending": 1, "overdue": 0, "capacity": 65},
        {"id": "pw-3", "name": "Ananya Reddy", "assigned": 9, "completed": 4, "pending": 2, "overdue": 3, "capacity": 92},
        {"id": "pw-4", "name": "Rahul Verma", "assigned": 6, "completed": 3, "pending": 2, "overdue": 1, "capacity": 58},
        {"id": "pw-5", "name": "Meera Nair", "assigned": 4, "completed": 3, "pending": 1, "overdue": 0, "capacity": 60},
        {"id": "pw-6", "name": "Karan Joshi", "assigned": 3, "completed": 1, "pending": 1, "overdue": 1, "capacity": 45},
    ]
    await db.pm_workload.insert_many(pm_workload)
    print(f"✅  Seeded {len(pm_workload)} PM workload entries")

    # PM — PMRiskEscalation.jsx
    pm_escalation_events = [
        {"id": "pe-1", "time": "Feb 20, 2026 10:30", "event": "Sprint Delta — deployment failure escalated", "who": "Ananya Reddy", "status": "Open", "severity": "High"},
        {"id": "pe-2", "time": "Feb 19, 2026 15:00", "event": "Design spec mismatch — Dashboard UI", "who": "Rahul Verma", "status": "In Progress", "severity": "Medium"},
        {"id": "pe-3", "time": "Feb 18, 2026 09:15", "event": "CI/CD pipeline broken for 4 hours", "who": "Ananya Reddy", "status": "Resolved", "severity": "High"},
        {"id": "pe-4", "time": "Feb 17, 2026 14:45", "event": "Dependency conflict in Auth module", "who": "Vikram Singh", "status": "Resolved", "severity": "Low"},
        {"id": "pe-5", "time": "Feb 16, 2026 11:00", "event": "Scope creep in Sprint Beta", "who": "Sneha Iyer", "status": "Resolved", "severity": "Medium"},
    ]
    await db.pm_escalation_events.insert_many(pm_escalation_events)
    print(f"✅  Seeded {len(pm_escalation_events)} PM escalation events")

    high_risk_members = [
        {"id": "hrm-1", "name": "Ananya Reddy", "escalations": 3, "avgDelay": "8.5h", "risk": "High"},
        {"id": "hrm-2", "name": "Karan Joshi", "escalations": 2, "avgDelay": "14h", "risk": "High"},
        {"id": "hrm-3", "name": "Rahul Verma", "escalations": 1, "avgDelay": "6h", "risk": "Medium"},
    ]
    await db.high_risk_members.insert_many(high_risk_members)
    print(f"✅  Seeded {len(high_risk_members)} high risk members")

    delay_distribution = [
        {"id": "dd-1", "range": "0-2h", "count": 8},
        {"id": "dd-2", "range": "2-6h", "count": 5},
        {"id": "dd-3", "range": "6-12h", "count": 3},
        {"id": "dd-4", "range": "12-24h", "count": 2},
        {"id": "dd-5", "range": "24h+", "count": 1},
    ]
    await db.delay_distribution.insert_many(delay_distribution)
    print(f"✅  Seeded {len(delay_distribution)} delay distribution buckets")

    # PM — PMRetrospective.jsx — owner+due (NOT assignee+deadline)
    pm_retro_summary = [
        {"id": "prs-1", "sprintName": "Sprint Alpha", "completionPct": 82, "alignmentAvg": 84.2, "behaviourAvg": 8.1, "bottleneck": "DevOps Pipeline"},
    ]
    await db.pm_retro_summary.insert_many(pm_retro_summary)
    print(f"✅  Seeded {len(pm_retro_summary)} PM retro summaries")

    pm_improvements = [
        {"id": "pi-1", "action": "Add pipeline health check before deployments", "owner": "Ananya Reddy", "due": "Sprint Beta"},
        {"id": "pi-2", "action": "Introduce daily standups for high-risk tasks", "owner": "Sneha Iyer", "due": "Sprint Beta"},
        {"id": "pi-3", "action": "Redistribute workload for overloaded members", "owner": "PM", "due": "Immediate"},
        {"id": "pi-4", "action": "Better sprint scoping with buffer for unknowns", "owner": "PM", "due": "Sprint Beta"},
    ]
    await db.pm_improvements.insert_many(pm_improvements)
    print(f"✅  Seeded {len(pm_improvements)} PM improvements")

    ai_retro_suggestions = [
        {"id": "ais-1", "text": "Reduce sprint scope by 15% to prevent spillover. Historical data shows 82% completion rate with current scoping.", "sprint": "Sprint Alpha"},
        {"id": "ais-2", "text": "Assign Karan Joshi as pair-programming partner with Vikram Singh to improve velocity by estimated 20%.", "sprint": "Sprint Alpha"},
        {"id": "ais-3", "text": "DevOps tasks should have a 2-hour buffer built into estimates based on pipeline instability patterns.", "sprint": "Sprint Alpha"},
        {"id": "ais-4", "text": "Consider splitting the Dashboard UI task into 3 smaller stories for better tracking and faster delivery.", "sprint": "Sprint Alpha"},
    ]
    await db.ai_retro_suggestions.insert_many(ai_retro_suggestions)
    print(f"✅  Seeded {len(ai_retro_suggestions)} AI retro suggestions")

    # ═══════════════════════════════════════════════════════════════
    # LEAD / SCRUM MASTER — SMSprintBoard.jsx
    # id, title, assignee, type, points, alignment, risk, reviewStatus, dueDate, status
    # ═══════════════════════════════════════════════════════════════
    sprint_stories = [
        {"id": "ST-101", "title": "Implement Auth Module", "assignee": "Vikram Singh", "type": "Dev", "points": 8, "alignment": 94, "risk": "Low", "reviewStatus": "Approved", "dueDate": "Feb 20", "status": "Done", "sprint": "Sprint Alpha"},
        {"id": "ST-102", "title": "Setup CI/CD Pipeline", "assignee": "Ananya Reddy", "type": "DevOps", "points": 8, "alignment": 78, "risk": "High", "reviewStatus": "Pending", "dueDate": "Feb 22", "status": "In Progress", "sprint": "Sprint Alpha"},
        {"id": "ST-103", "title": "User Profile API", "assignee": "Vikram Singh", "type": "Dev", "points": 5, "alignment": 88, "risk": "Low", "reviewStatus": "In Review", "dueDate": "Feb 21", "status": "In Review", "sprint": "Sprint Alpha"},
        {"id": "ST-104", "title": "Dashboard UI Redesign", "assignee": "Rahul Verma", "type": "Dev", "points": 8, "alignment": 65, "risk": "High", "reviewStatus": "Pending", "dueDate": "Feb 23", "status": "In Progress", "sprint": "Sprint Alpha"},
        {"id": "ST-105", "title": "Integration Tests – Sprint API", "assignee": "Meera Nair", "type": "QA", "points": 5, "alignment": 85, "risk": "Low", "reviewStatus": "Approved", "dueDate": "Feb 19", "status": "Done", "sprint": "Sprint Alpha"},
        {"id": "ST-106", "title": "Database Migration Script", "assignee": "Ananya Reddy", "type": "DevOps", "points": 5, "alignment": 72, "risk": "Medium", "reviewStatus": "Pending", "dueDate": "Feb 22", "status": "In Progress", "sprint": "Sprint Alpha"},
        {"id": "ST-107", "title": "Notification Service", "assignee": "Karan Joshi", "type": "Dev", "points": 8, "alignment": 58, "risk": "High", "reviewStatus": "Rejected", "dueDate": "Feb 28", "status": "Blocked", "sprint": "Sprint Alpha"},
        {"id": "ST-108", "title": "Load Testing Setup", "assignee": "Meera Nair", "type": "QA", "points": 5, "alignment": 90, "risk": "Low", "reviewStatus": "Approved", "dueDate": "Feb 20", "status": "Done", "sprint": "Sprint Alpha"},
        {"id": "ST-109", "title": "API Rate Limiting", "assignee": "Vikram Singh", "type": "Dev", "points": 4, "alignment": 82, "risk": "Low", "reviewStatus": "In Review", "dueDate": "Feb 22", "status": "In Review", "sprint": "Sprint Alpha"},
        {"id": "ST-110", "title": "Monitoring Dashboard", "assignee": "Ananya Reddy", "type": "DevOps", "points": 5, "alignment": 70, "risk": "Medium", "reviewStatus": "Pending", "dueDate": "Feb 24", "status": "To Do", "sprint": "Sprint Alpha"},
    ]
    await db.sprint_stories.insert_many(sprint_stories)
    print(f"✅  Seeded {len(sprint_stories)} sprint stories")

    lead_retrospectives = [
        {
            "id": "lr-1", "sprint": "Sprint Alpha",
            "wellNotes": [
                "OAuth2 integration completed ahead of schedule with zero defects.",
                "Cross-team collaboration between Dev and DevOps improved significantly.",
                "Code review turnaround time reduced from 24h to 6h avg.",
                "All acceptance criteria were well-defined before sprint start.",
            ],
            "didntNotes": [
                "SSO provider config was blocked by external dependency for 48+ hours.",
                "CI/CD pipeline staging delayed due to infrastructure provisioning gaps.",
                "MFA design spec changed mid-sprint, causing scope drift.",
                "Workload imbalance – Ananya R. had 3x more DevOps stories than planned.",
            ],
            "actionNotes": [
                "Pre-provision staging environments before sprint start",
                "Lock acceptance criteria 2 days before sprint planning",
                "Add auto-assign for code reviews with 4h SLA",
                "Weekly workload rebalancing check-in",
            ],
            "aiSummary": "Sprint Alpha achieved an 81.7% completion rate with 98 of 120 story points delivered.",
        }
    ]
    await db.lead_retrospectives.insert_many(lead_retrospectives)
    print(f"✅  Seeded {len(lead_retrospectives)} lead retrospectives")

    # ═══════════════════════════════════════════════════════════════
    # DEVELOPER — Pull Requests, Branches, Submissions
    # ═══════════════════════════════════════════════════════════════
    pull_requests = [
        {"id": "PR-201", "title": "feat: implement OAuth2 login flow", "author": "Vikram Singh", "branch": "feature/oauth2-login", "base": "develop", "status": "Open", "reviewStatus": "Approved", "comments": 4, "changedFiles": 7, "additions": 142, "deletions": 18, "createdAt": "Feb 18, 2026", "sprint": "Sprint Alpha"},
        {"id": "PR-202", "title": "fix: correct JWT expiry handling", "author": "Vikram Singh", "branch": "fix/jwt-expiry", "base": "develop", "status": "Merged", "reviewStatus": "Approved", "comments": 2, "changedFiles": 3, "additions": 24, "deletions": 6, "createdAt": "Feb 17, 2026", "sprint": "Sprint Alpha"},
        {"id": "PR-203", "title": "feat: user profile API endpoints", "author": "Vikram Singh", "branch": "feature/user-profile-api", "base": "develop", "status": "Open", "reviewStatus": "In Review", "comments": 6, "changedFiles": 9, "additions": 210, "deletions": 32, "createdAt": "Feb 19, 2026", "sprint": "Sprint Alpha"},
    ]
    await db.pull_requests.insert_many(pull_requests)
    print(f"✅  Seeded {len(pull_requests)} pull requests")

    branches = [
        {"id": "br-1", "name": "feature/oauth2-login", "author": "Vikram Singh", "status": "Active", "lastCommit": "2h ago", "commits": 12, "aheadBy": 3, "behindBy": 0, "ciStatus": "Passing", "sprint": "Sprint Alpha"},
        {"id": "br-2", "name": "fix/jwt-expiry", "author": "Vikram Singh", "status": "Merged", "lastCommit": "1 day ago", "commits": 4, "aheadBy": 0, "behindBy": 0, "ciStatus": "Passing", "sprint": "Sprint Alpha"},
        {"id": "br-3", "name": "feature/user-profile-api", "author": "Vikram Singh", "status": "Active", "lastCommit": "4h ago", "commits": 8, "aheadBy": 5, "behindBy": 1, "ciStatus": "Running", "sprint": "Sprint Alpha"},
    ]
    await db.branches.insert_many(branches)
    print(f"✅  Seeded {len(branches)} branches")

    submissions = [
        {"id": "sub-1", "storyId": "ST-101", "title": "Implement Auth Module", "submittedBy": "Vikram Singh", "submittedAt": "Feb 20, 2026", "status": "Approved", "reviewedBy": "Sneha Iyer", "tab": "completed", "aiScore": 91, "comments": "Clean implementation, well tested."},
        {"id": "sub-2", "storyId": "ST-103", "title": "User Profile API", "submittedBy": "Vikram Singh", "submittedAt": "Feb 21, 2026", "status": "In Review", "reviewedBy": "", "tab": "pending", "aiScore": 84, "comments": ""},
    ]
    await db.submissions.insert_many(submissions)
    print(f"✅  Seeded {len(submissions)} submissions")

    # ═══════════════════════════════════════════════════════════════
    # DEVOPS — Incidents, Infra Changes, Logs, Tasks
    # ═══════════════════════════════════════════════════════════════
    incidents = [
        {"id": "INC-001", "incident": "API Gateway returning 502 errors for /auth/login endpoint", "severity": "Critical", "service": "Auth Service", "openedAt": "Feb 20, 10:30", "resolvedAt": "Feb 20, 12:15", "rootCause": "Memory leak in Node.js auth service", "mttd": "8m", "mttr": "1h 45m", "repeat": False, "aiSummary": "Memory leak caused cascading 502 errors. Resolved by recycling auth pods."},
        {"id": "INC-002", "incident": "Database connection pool exhausted — 503 errors on all services", "severity": "High", "service": "Database", "openedAt": "Feb 19, 14:20", "resolvedAt": "Feb 19, 15:05", "rootCause": "Misconfigured max connections in connection pool", "mttd": "12m", "mttr": "45m", "repeat": True, "aiSummary": "Second occurrence this sprint. Connection pool config must be reviewed."},
        {"id": "INC-003", "incident": "CI/CD pipeline timeout causing failed deployments", "severity": "Medium", "service": "DevOps Pipeline", "openedAt": "Feb 18, 09:00", "resolvedAt": "Feb 18, 11:30", "rootCause": "Insufficient timeout threshold for large Docker builds", "mttd": "5m", "mttr": "2h 30m", "repeat": False, "aiSummary": "Timeout threshold adjusted. Build caching enabled to prevent recurrence."},
    ]
    await db.incidents.insert_many(incidents)
    print(f"✅  Seeded {len(incidents)} incidents")

    infra_changes = [
        {"id": 1, "type": "Docker Config Update", "service": "Auth Service", "changedBy": "Ananya Reddy", "timestamp": "Feb 20, 2026 10:45", "risk": "Low", "approved": True, "details": "Updated memory limits to 512MB"},
        {"id": 2, "type": "Kubernetes Scaling", "service": "API Gateway", "changedBy": "Ananya Reddy", "timestamp": "Feb 19, 2026 15:30", "risk": "Medium", "approved": True, "details": "Scaled replicas from 2 to 4"},
        {"id": 3, "type": "Environment Variable", "service": "Database", "changedBy": "Ananya Reddy", "timestamp": "Feb 18, 2026 09:15", "risk": "High", "approved": False, "details": "Changed DB_MAX_CONNECTIONS from 50 to 200"},
        {"id": 4, "type": "Terraform Modification", "service": "VPC", "changedBy": "Ananya Reddy", "timestamp": "Feb 17, 2026 14:00", "risk": "High", "approved": True, "details": "Added private subnet for database tier"},
    ]
    await db.infra_changes.insert_many(infra_changes)
    print(f"✅  Seeded {len(infra_changes)} infra changes")

    logs_alerts = [
        {"id": 1, "category": "Error", "severity": "Critical", "service": "Auth Service", "message": "FATAL: Out of memory — process killed", "timestamp": "Feb 20, 10:22 AM", "count": 3},
        {"id": 2, "category": "Warning", "severity": "High", "service": "Database", "message": "Connection pool at 95% capacity", "timestamp": "Feb 20, 10:18 AM", "count": 12},
        {"id": 3, "category": "Security", "severity": "High", "service": "API Gateway", "message": "Rate limit exceeded from IP 192.168.1.45", "timestamp": "Feb 20, 09:55 AM", "count": 847},
        {"id": 4, "category": "Memory", "severity": "Medium", "service": "Notification Service", "message": "Memory usage at 78% — approaching threshold", "timestamp": "Feb 20, 09:40 AM", "count": 1},
        {"id": 5, "category": "Error", "severity": "Low", "service": "Report Service", "message": "Timeout generating PDF for user report", "timestamp": "Feb 20, 09:15 AM", "count": 2},
    ]
    await db.logs_alerts.insert_many(logs_alerts)
    print(f"✅  Seeded {len(logs_alerts)} log alerts")

    log_ai_analysis = [
        {"id": "ai-1", "text": "Memory leak detected in Auth Service — pod cycling recommended immediately.", "type": "danger"},
        {"id": "ai-2", "text": "Database connection pool config appears too low for current traffic. Recommend increasing to 150.", "type": "warning"},
        {"id": "ai-3", "text": "CI/CD pipeline performance improved 22% after caching changes applied yesterday.", "type": "success"},
    ]
    await db.log_ai_analysis.insert_many(log_ai_analysis)
    print(f"✅  Seeded {len(log_ai_analysis)} log AI analysis entries")

    devops_tasks = [
        {"id": 1, "story": "Setup CI/CD pipeline for Sprint Beta", "type": "Deployment", "env": "Staging", "status": "In Progress", "alignment": 78, "ciAligned": True, "deployTriggered": False, "filesCorrect": True, "aiNote": "Pipeline config looks aligned but staging infra not provisioned."},
        {"id": 2, "story": "Configure auto-scaling for API Gateway", "type": "Infra Change", "env": "Production", "status": "Done", "alignment": 92, "ciAligned": True, "deployTriggered": True, "filesCorrect": True, "aiNote": "Scaling policies properly configured. Zero downtime deployment."},
        {"id": 3, "story": "Set up Prometheus monitoring dashboard", "type": "Monitoring Setup", "env": "All", "status": "To Do", "alignment": 65, "ciAligned": False, "deployTriggered": False, "filesCorrect": False, "aiNote": "Monitoring config missing from Sprint plan — needs alignment review."},
        {"id": 4, "story": "Patch CVE-2024-0012 in Node.js dependencies", "type": "Security Patch", "env": "Dev", "status": "Done", "alignment": 95, "ciAligned": True, "deployTriggered": True, "filesCorrect": True, "aiNote": "Vulnerability patched. All downstream services tested and passing."},
    ]
    await db.devops_tasks.insert_many(devops_tasks)
    print(f"✅  Seeded {len(devops_tasks)} devops tasks")

    # ═══════════════════════════════════════════════════════════════
    # QA — Test Cases, Bugs, Assigned Stories, Regression, Release, Quality, Runs
    # ═══════════════════════════════════════════════════════════════
    test_cases = [
        {"id": "TC-001", "title": "Verify login with valid credentials", "story": "US-101", "type": "Functional", "priority": "Critical", "status": "Passed", "steps": 4, "updatedAt": "Feb 20"},
        {"id": "TC-002", "title": "Verify login blocks after 5 failed attempts", "story": "US-101", "type": "Negative", "priority": "High", "status": "Passed", "steps": 6, "updatedAt": "Feb 20"},
        {"id": "TC-003", "title": "OAuth2 provider redirect flow", "story": "US-102", "type": "Integration", "priority": "High", "status": "In Progress", "steps": 8, "updatedAt": "Feb 19"},
        {"id": "TC-004", "title": "Profile API response time < 200ms", "story": "US-103", "type": "Performance", "priority": "Medium", "status": "Pending", "steps": 3, "updatedAt": "Feb 18"},
        {"id": "TC-005", "title": "MFA with 6-digit TOTP code", "story": "US-106", "type": "Functional", "priority": "Critical", "status": "Failed", "steps": 5, "updatedAt": "Feb 21"},
    ]
    await db.test_cases.insert_many(test_cases)
    print(f"✅  Seeded {len(test_cases)} test cases")

    bugs_qa = [
        {
            "id": "BUG-001", "story": "US-101", "severity": "Critical", "status": "Open",
            "assignedTo": "Vikram Singh", "reopenCount": 0,
            "summary": "Login fails with correct credentials after password reset",
            "env": "Staging",
            "steps": ["Log in with original password", "Use 'Forgot Password' to reset", "Try login with new password — fails with 401"],
            "hasScreenshot": True, "hasLogs": True,
        },
        {
            "id": "BUG-002", "story": "US-102", "severity": "High", "status": "In Progress",
            "assignedTo": "Ananya Reddy", "reopenCount": 1,
            "summary": "OAuth2 redirect returns 404 on staging environment only",
            "env": "Staging",
            "steps": ["Click 'Login with Google'", "OAuth2 redirects to /auth/callback", "Staging returns 404 — works in Dev"],
            "hasScreenshot": False, "hasLogs": True,
        },
        {
            "id": "BUG-003", "story": "US-103", "severity": "Medium", "status": "Resolved",
            "assignedTo": "Vikram Singh", "reopenCount": 2,
            "summary": "Profile image upload silently fails for files > 2MB",
            "env": "Dev",
            "steps": ["Navigate to profile settings", "Upload image > 2MB", "No error shown, but image not saved"],
            "hasScreenshot": True, "hasLogs": False,
        },
    ]
    await db.bugs_qa.insert_many(bugs_qa)
    print(f"✅  Seeded {len(bugs_qa)} QA bugs")

    assigned_stories = [
        {"id": 1, "story": "Implement OAuth2 login flow", "developer": "Vikram Singh", "buildVersion": "v1.4.2", "alignment": 94, "testStatus": "Passed", "priority": "Critical", "deadline": "Feb 20", "acceptance": ["OAuth2 redirect works", "Token stored in httpOnly cookie", "Session expires after 24h"], "linkedPR": "PR-201", "buildEnv": "Staging"},
        {"id": 2, "story": "Setup CI/CD pipeline", "developer": "Ananya Reddy", "buildVersion": "v1.4.1", "alignment": 78, "testStatus": "Testing", "priority": "High", "deadline": "Feb 22", "acceptance": ["Pipeline triggers on PR merge", "Tests run automatically", "Staging deploys on green"], "linkedPR": "PR-202", "buildEnv": "Dev"},
        {"id": 3, "story": "User Profile API", "developer": "Vikram Singh", "buildVersion": "v1.4.3", "alignment": 88, "testStatus": "Pending", "priority": "Medium", "deadline": "Feb 21", "acceptance": ["GET /profile returns user data", "PATCH /profile updates fields", "Response time < 200ms"], "linkedPR": "PR-203", "buildEnv": "Staging"},
    ]
    await db.assigned_stories.insert_many(assigned_stories)
    print(f"✅  Seeded {len(assigned_stories)} assigned stories")

    regression_suites = [
        {"id": "REG-001", "module": "Authentication", "cases": 42, "passed": 40, "failed": 2, "flaky": False, "lastRun": "2h ago"},
        {"id": "REG-002", "module": "User Management", "cases": 28, "passed": 26, "failed": 1, "flaky": True, "lastRun": "4h ago"},
        {"id": "REG-003", "module": "API Gateway", "cases": 35, "passed": 35, "failed": 0, "flaky": False, "lastRun": "1h ago"},
        {"id": "REG-004", "module": "Notifications", "cases": 18, "passed": 12, "failed": 4, "flaky": True, "lastRun": "6h ago"},
        {"id": "REG-005", "module": "Reports", "cases": 22, "passed": 20, "failed": 2, "flaky": False, "lastRun": "3h ago"},
    ]
    await db.regression_suites.insert_many(regression_suites)
    print(f"✅  Seeded {len(regression_suites)} regression suites")

    release_checks = [
        {"label": "Test Pass Rate", "value": 94, "threshold": 90, "status": "pass"},
        {"label": "Code Coverage", "value": 82, "threshold": 80, "status": "pass"},
        {"label": "Critical Bugs Open", "value": 1, "threshold": 0, "status": "fail"},
        {"label": "Performance Baseline", "value": "185ms", "threshold": "200ms", "status": "pass"},
        {"label": "Security Scan", "value": "2 warnings", "threshold": "0 critical", "status": "warning"},
    ]
    await db.release_checks.insert_many(release_checks)
    print(f"✅  Seeded {len(release_checks)} release checks")

    blocking_bugs = [
        {"id": "BUG-001", "summary": "Login fails after password reset", "severity": "Critical", "service": "Auth Service"},
    ]
    await db.blocking_bugs.insert_many(blocking_bugs)
    print(f"✅  Seeded {len(blocking_bugs)} blocking bugs")

    quality_metrics = [
        {"id": "qm-1", "label": "Sprint Completion", "weight": "40%", "value": 82, "color": "#10b981"},
        {"id": "qm-2", "label": "Alignment Accuracy", "weight": "30%", "value": 87, "color": "#3b82f6"},
        {"id": "qm-3", "label": "Behaviour Score", "weight": "20%", "value": 84, "color": "#8b5cf6"},
        {"id": "qm-4", "label": "Delivery Speed", "weight": "10%", "value": 76, "color": "#f59e0b"},
    ]
    await db.quality_metrics.insert_many(quality_metrics)
    print(f"✅  Seeded {len(quality_metrics)} quality metrics")

    test_runs = [
        {"id": 1, "build": "v1.4.2", "env": "Staging", "total": 145, "passed": 138, "failed": 7, "duration": "12m 34s", "ciStatus": "Passing", "coverage": 82},
        {"id": 2, "build": "v1.4.1", "env": "Dev", "total": 145, "passed": 140, "failed": 5, "duration": "11m 58s", "ciStatus": "Passing", "coverage": 80},
        {"id": 3, "build": "v1.4.0", "env": "Production", "total": 120, "passed": 118, "failed": 2, "duration": "9m 45s", "ciStatus": "Passing", "coverage": 78},
    ]
    await db.test_runs.insert_many(test_runs)
    print(f"✅  Seeded {len(test_runs)} test runs")

    # ═══════════════════════════════════════════════════════════════
    # HR — Behaviour, Candidates, Performance, Audit, Reports, Settings
    # ═══════════════════════════════════════════════════════════════
    behaviour_history = [
        {"id": "bh-1", "month": "Dec 2025", "member": "Vikram Singh", "score": 8.2, "ratedBy": "Priya Sharma"},
        {"id": "bh-2", "month": "Jan 2026", "member": "Vikram Singh", "score": 8.5, "ratedBy": "Priya Sharma"},
        {"id": "bh-3", "month": "Feb 2026", "member": "Vikram Singh", "score": 8.7, "ratedBy": "Priya Sharma"},
        {"id": "bh-4", "month": "Dec 2025", "member": "Ananya Reddy", "score": 7.5, "ratedBy": "Priya Sharma"},
        {"id": "bh-5", "month": "Jan 2026", "member": "Ananya Reddy", "score": 7.2, "ratedBy": "Priya Sharma"},
        {"id": "bh-6", "month": "Feb 2026", "member": "Ananya Reddy", "score": 7.8, "ratedBy": "Priya Sharma"},
    ]
    await db.behaviour_history.insert_many(behaviour_history)
    print(f"✅  Seeded {len(behaviour_history)} behaviour history entries")

    # Note: 'collaboration' NOT 'teamwork' — verified from HRBehaviourScores.jsx criteria array
    behaviour_ratings = [
        {"id": "br-1", "member": "Vikram Singh", "sprint": "Sprint Alpha", "communication": 4, "ownership": 5, "collaboration": 4, "leadership": 4, "discipline": 5, "comment": "Excellent sprint.", "ratedBy": "Sneha Iyer"},
        {"id": "br-2", "member": "Ananya Reddy", "sprint": "Sprint Alpha", "communication": 3, "ownership": 4, "collaboration": 3, "leadership": 3, "discipline": 4, "comment": "Workload was too high.", "ratedBy": "Sneha Iyer"},
        {"id": "br-3", "member": "Sneha Iyer", "sprint": "Sprint Alpha", "communication": 5, "ownership": 4, "collaboration": 5, "leadership": 4, "discipline": 5, "comment": "Great facilitation.", "ratedBy": "Arjun Patel"},
    ]
    await db.behaviour_ratings.insert_many(behaviour_ratings)
    print(f"✅  Seeded {len(behaviour_ratings)} behaviour ratings")

    candidates = [
        {"id": 1, "name": "Ravi Kumar", "email": "ravi.kumar@gmail.com", "role": "Developer", "dept": "Engineering", "project": "Sprint Beta", "appliedDate": "Feb 15, 2026", "status": "Interview", "experience": "4 years"},
        {"id": 2, "name": "Nisha Patel", "email": "nisha.patel@gmail.com", "role": "DevOps", "dept": "Infrastructure", "project": "—", "appliedDate": "Feb 12, 2026", "status": "Screening", "experience": "3 years"},
        {"id": 3, "name": "Aakash Gupta", "email": "aakash.gupta@gmail.com", "role": "QA Engineer", "dept": "Quality Assurance", "project": "Sprint Beta", "appliedDate": "Feb 10, 2026", "status": "Offer Sent", "experience": "5 years"},
        {"id": 4, "name": "Lakshmi Rao", "email": "lakshmi.rao@gmail.com", "role": "HR Manager", "dept": "Human Resources", "project": "—", "appliedDate": "Feb 8, 2026", "status": "Hired", "experience": "7 years"},
    ]
    await db.candidates.insert_many(candidates)
    print(f"✅  Seeded {len(candidates)} candidates")

    dept_performance = [
        {"id": "dp-1", "dept": "Engineering", "score": 87.5},
        {"id": "dp-2", "dept": "DevOps", "score": 74.3},
        {"id": "dp-3", "dept": "QA", "score": 82.1},
        {"id": "dp-4", "dept": "HR", "score": 88.0},
        {"id": "dp-5", "dept": "Management", "score": 85.5},
    ]
    await db.dept_performance.insert_many(dept_performance)
    print(f"✅  Seeded {len(dept_performance)} dept performance entries")

    sprint_velocity = [
        {"id": "sv-1", "sprint": "Sprint Delta", "planned": 60, "completed": 47},
        {"id": "sv-2", "sprint": "Sprint Gamma", "planned": 55, "completed": 52},
        {"id": "sv-3", "sprint": "Sprint Beta", "planned": 65, "completed": 58},
        {"id": "sv-4", "sprint": "Sprint Alpha", "planned": 60, "completed": 49},
    ]
    await db.sprint_velocity.insert_many(sprint_velocity)
    print(f"✅  Seeded {len(sprint_velocity)} sprint velocity records")

    performers = [
        {"id": "perf-1", "name": "Vikram Singh", "score": 89.2, "role": "Developer", "issue": "", "type": "top"},
        {"id": "perf-2", "name": "Priya Sharma", "score": 88.1, "role": "HR", "issue": "", "type": "top"},
        {"id": "perf-3", "name": "Arjun Patel", "score": 85.5, "role": "Sprint Master", "issue": "", "type": "top"},
        {"id": "perf-4", "name": "Ananya Reddy", "score": 74.3, "role": "DevOps", "issue": "Workload distribution", "type": "low"},
        {"id": "perf-5", "name": "Karan Joshi", "score": 68.5, "role": "Developer", "issue": "3 overdue tasks this sprint", "type": "low"},
    ]
    await db.performers.insert_many(performers)
    print(f"✅  Seeded {len(performers)} performers")

    audit_log = [
        {"id": "al-1", "action": "Promotion Approved", "name": "Vikram Singh", "by": "Rajesh Mehta", "time": "Feb 20, 2026 11:30"},
        {"id": "al-2", "action": "Promotion Rejected", "name": "Karan Joshi", "by": "Rajesh Mehta", "time": "Feb 20, 2026 11:35"},
        {"id": "al-3", "action": "Weight Updated", "name": "Performance Weights", "by": "Priya Sharma", "time": "Feb 19, 2026 14:00"},
        {"id": "al-4", "action": "Candidate Hired", "name": "Lakshmi Rao", "by": "Priya Sharma", "time": "Feb 18, 2026 10:15"},
    ]
    await db.audit_log.insert_many(audit_log)
    print(f"✅  Seeded {len(audit_log)} audit log entries")

    hr_reports = [
        {"id": 1, "title": "Sprint Performance Report", "desc": "Comprehensive analysis of sprint completion rates and team velocity.", "color": "#3b82f6", "lastGenerated": "Feb 20, 2026"},
        {"id": 2, "title": "Behaviour Score Report", "desc": "Monthly behaviour assessment scores across all team members.", "color": "#8b5cf6", "lastGenerated": "Feb 18, 2026"},
        {"id": 3, "title": "Promotion Eligibility Report", "desc": "AI-powered promotion recommendations based on performance scores.", "color": "#10b981", "lastGenerated": "Feb 15, 2026"},
        {"id": 4, "title": "Hiring Pipeline Report", "desc": "Candidate status, onboarding progress, and hiring funnel analysis.", "color": "#f59e0b", "lastGenerated": "Feb 17, 2026"},
    ]
    await db.hr_reports.insert_many(hr_reports)
    print(f"✅  Seeded {len(hr_reports)} HR reports")

    company_settings = [
        {
            "id": "settings-001",
            "company": {"name": "Exactiomark", "domain": "exactiomark.com", "industry": "Software Development", "location": "Bengaluru, India"},
            "weights": {"sprint": 40, "alignment": 30, "delivery": 20, "behaviour": 10},
            "sprintPolicy": {"duration": 14, "maxSP": 65, "approvalSLA": 4},
            "behaviourAssign": ["LEAD", "PM", "HR"],
            "promotionWeightEdit": ["HR", "CEO"],
        }
    ]
    await db.company_settings.insert_many(company_settings)
    print(f"✅  Seeded company settings")

    print("\n==== PHASE 3: Lead / Scrum Master Page Collections ====\n")

    # ── LeadDashboard.jsx ──────────────────────────────────────────────────────
    lead_team_members = [
        {"id": 1, "name": "Vikram Singh", "role": "Senior Developer", "tasks": 8, "completed": 5, "status": "Active"},
        {"id": 2, "name": "Ravi Kumar", "role": "Developer", "tasks": 6, "completed": 4, "status": "Active"},
        {"id": 3, "name": "Meera Joshi", "role": "Junior Developer", "tasks": 5, "completed": 3, "status": "Active"},
        {"id": 4, "name": "Deepak Nair", "role": "QA Engineer", "tasks": 7, "completed": 6, "status": "On Leave"},
        {"id": 5, "name": "Pooja Gupta", "role": "Developer", "tasks": 6, "completed": 2, "status": "Active"},
    ]
    await db.lead_team_members.insert_many(lead_team_members)
    print(f"✅  Seeded {len(lead_team_members)} lead team members")

    lead_workload_chart = [
        {"id": "lwc-1", "name": "Vikram", "assigned": 8, "completed": 5},
        {"id": "lwc-2", "name": "Ravi", "assigned": 6, "completed": 4},
        {"id": "lwc-3", "name": "Meera", "assigned": 5, "completed": 3},
        {"id": "lwc-4", "name": "Deepak", "assigned": 7, "completed": 6},
        {"id": "lwc-5", "name": "Pooja", "assigned": 6, "completed": 2},
    ]
    await db.lead_workload_chart.insert_many(lead_workload_chart)
    print(f"✅  Seeded {len(lead_workload_chart)} lead workload chart entries")

    lead_perf_trend = [
        {"id": "lpt-1", "week": "W1", "score": 72},
        {"id": "lpt-2", "week": "W2", "score": 76},
        {"id": "lpt-3", "week": "W3", "score": 74},
        {"id": "lpt-4", "week": "W4", "score": 81},
        {"id": "lpt-5", "week": "W5", "score": 85},
        {"id": "lpt-6", "week": "W6", "score": 88},
    ]
    await db.lead_perf_trend.insert_many(lead_perf_trend)
    print(f"✅  Seeded {len(lead_perf_trend)} lead perf trend weeks")

    lead_review_queue = [
        {"id": 1, "title": "PR #342 – Refactor auth middleware", "author": "Vikram Singh", "priority": "High", "submitted": "2h ago"},
        {"id": 2, "title": "PR #340 – Add pagination to user list", "author": "Ravi Kumar", "priority": "Medium", "submitted": "5h ago"},
        {"id": 3, "title": "PR #338 – Fix date picker timezone bug", "author": "Meera Joshi", "priority": "Low", "submitted": "1d ago"},
        {"id": 4, "title": "Task Review – Sprint planning doc", "author": "Pooja Gupta", "priority": "Medium", "submitted": "1d ago"},
    ]
    await db.lead_review_queue.insert_many(lead_review_queue)
    print(f"✅  Seeded {len(lead_review_queue)} lead review queue items")

    # ── SMAlignmentInsights.jsx ────────────────────────────────────────────────
    alignment_breakdown = [
        {"id": "ab-1", "name": "Vikram Singh", "keyword": 92, "filePath": 88, "semantic": 91, "scopeDrift": 4},
        {"id": "ab-2", "name": "Ananya Reddy", "keyword": 75, "filePath": 70, "semantic": 78, "scopeDrift": 18},
        {"id": "ab-3", "name": "Rahul Verma", "keyword": 60, "filePath": 58, "semantic": 65, "scopeDrift": 28},
        {"id": "ab-4", "name": "Meera Nair", "keyword": 89, "filePath": 85, "semantic": 87, "scopeDrift": 5},
        {"id": "ab-5", "name": "Karan Joshi", "keyword": 55, "filePath": 52, "semantic": 58, "scopeDrift": 35},
    ]
    await db.alignment_breakdown.insert_many(alignment_breakdown)
    print(f"✅  Seeded {len(alignment_breakdown)} alignment breakdown entries")

    low_alignment_stories = [
        {"id": "ST-107", "title": "Notification Service", "developer": "Karan Joshi", "alignment": 42, "offenses": 3, "note": "Repeat offender — 3 sprints below 60%"},
        {"id": "ST-104", "title": "Dashboard UI Redesign", "developer": "Rahul Verma", "alignment": 65, "offenses": 2, "note": "Scope drift in UI layer consistently"},
        {"id": "ST-106", "title": "Database Migration Script", "developer": "Ananya Reddy", "alignment": 72, "offenses": 1, "note": "Schema diverged from original spec"},
        {"id": "ST-102", "title": "Setup CI/CD Pipeline", "developer": "Ananya Reddy", "alignment": 78, "offenses": 1, "note": "DevOps config scope drift"},
        {"id": "ST-110", "title": "Monitoring Dashboard", "developer": "Ananya Reddy", "alignment": 70, "offenses": 1, "note": "Dashboard spec mismatch"},
    ]
    await db.low_alignment_stories.insert_many(low_alignment_stories)
    print(f"✅  Seeded {len(low_alignment_stories)} low alignment stories")

    alignment_trend = [
        {"id": "at-1", "sprint": "S1", "avg": 74},
        {"id": "at-2", "sprint": "S2", "avg": 76},
        {"id": "at-3", "sprint": "S3", "avg": 78},
        {"id": "at-4", "sprint": "S4", "avg": 75},
        {"id": "at-5", "sprint": "S5", "avg": 79},
        {"id": "at-6", "sprint": "S6", "avg": 80},
    ]
    await db.alignment_trend.insert_many(alignment_trend)
    print(f"✅  Seeded {len(alignment_trend)} alignment trend points")

    # ── SMMyTeam.jsx ───────────────────────────────────────────────────────────
    # id, name, role, avatar, activeStories, alignmentAvg, risk, workload, status,
    # behaviourScore, sprintStories[], alignmentHistory[], rejectionRate,
    # blockerInvolvement, behaviourNotes, workloadHistory[]
    team_members_detail = [
        {
            "id": 1, "name": "Vikram Singh", "role": "Developer", "avatar": "VS",
            "activeStories": 3, "alignmentAvg": 91, "risk": "Low", "workload": 72,
            "status": "Active", "behaviourScore": 8.5,
            "sprintStories": [
                {"id": "ST-101", "title": "Implement Auth Module", "points": 8, "status": "Done", "alignment": 94},
                {"id": "ST-103", "title": "User Profile API", "points": 5, "status": "In Review", "alignment": 88},
                {"id": "ST-109", "title": "API Rate Limiting", "points": 4, "status": "In Progress", "alignment": 82},
            ],
            "alignmentHistory": [
                {"sprint": "S1", "score": 78}, {"sprint": "S2", "score": 82},
                {"sprint": "S3", "score": 85}, {"sprint": "S4", "score": 88},
                {"sprint": "S5", "score": 90}, {"sprint": "S6", "score": 91},
            ],
            "rejectionRate": 5, "blockerInvolvement": 1,
            "behaviourNotes": "Consistently delivers high-quality code. Excellent problem solver and proactive communicator.",
            "workloadHistory": [
                {"sprint": "S1", "load": 60}, {"sprint": "S2", "load": 65},
                {"sprint": "S3", "load": 70}, {"sprint": "S4", "load": 68},
                {"sprint": "S5", "load": 72}, {"sprint": "S6", "load": 72},
            ],
        },
        {
            "id": 2, "name": "Ananya Reddy", "role": "DevOps Engineer", "avatar": "AR",
            "activeStories": 3, "alignmentAvg": 73, "risk": "High", "workload": 92,
            "status": "Active", "behaviourScore": 7.5,
            "sprintStories": [
                {"id": "ST-102", "title": "Setup CI/CD Pipeline", "points": 8, "status": "In Progress", "alignment": 78},
                {"id": "ST-106", "title": "Database Migration Script", "points": 5, "status": "In Progress", "alignment": 72},
                {"id": "ST-110", "title": "Monitoring Dashboard", "points": 5, "status": "To Do", "alignment": 70},
            ],
            "alignmentHistory": [
                {"sprint": "S1", "score": 82}, {"sprint": "S2", "score": 80},
                {"sprint": "S3", "score": 78}, {"sprint": "S4", "score": 75},
                {"sprint": "S5", "score": 73}, {"sprint": "S6", "score": 73},
            ],
            "rejectionRate": 15, "blockerInvolvement": 3,
            "behaviourNotes": "Technically strong but overloaded. Needs workload redistribution and scope review.",
            "workloadHistory": [
                {"sprint": "S1", "load": 70}, {"sprint": "S2", "load": 80},
                {"sprint": "S3", "load": 85}, {"sprint": "S4", "load": 88},
                {"sprint": "S5", "load": 90}, {"sprint": "S6", "load": 92},
            ],
        },
        {
            "id": 3, "name": "Rahul Verma", "role": "Developer", "avatar": "RV",
            "activeStories": 2, "alignmentAvg": 65, "risk": "High", "workload": 58,
            "status": "Active", "behaviourScore": 6.8,
            "sprintStories": [
                {"id": "ST-104", "title": "Dashboard UI Redesign", "points": 8, "status": "In Progress", "alignment": 65},
                {"id": "ST-107", "title": "Notification Service", "points": 5, "status": "To Do", "alignment": 58},
            ],
            "alignmentHistory": [
                {"sprint": "S1", "score": 72}, {"sprint": "S2", "score": 70},
                {"sprint": "S3", "score": 68}, {"sprint": "S4", "score": 66},
                {"sprint": "S5", "score": 65}, {"sprint": "S6", "score": 65},
            ],
            "rejectionRate": 18, "blockerInvolvement": 2,
            "behaviourNotes": "Struggling with alignment on UI tasks. Needs PM clarity on scope before story assignment.",
            "workloadHistory": [
                {"sprint": "S1", "load": 65}, {"sprint": "S2", "load": 62},
                {"sprint": "S3", "load": 60}, {"sprint": "S4", "load": 58},
                {"sprint": "S5", "load": 58}, {"sprint": "S6", "load": 58},
            ],
        },
        {
            "id": 4, "name": "Meera Nair", "role": "QA Engineer", "avatar": "MN",
            "activeStories": 2, "alignmentAvg": 87, "risk": "Low", "workload": 60,
            "status": "Active", "behaviourScore": 9.0,
            "sprintStories": [
                {"id": "ST-105", "title": "Integration Tests – Sprint API", "points": 5, "status": "Done", "alignment": 85},
                {"id": "ST-108", "title": "Load Testing Setup", "points": 5, "status": "Done", "alignment": 90},
            ],
            "alignmentHistory": [
                {"sprint": "S1", "score": 80}, {"sprint": "S2", "score": 82},
                {"sprint": "S3", "score": 84}, {"sprint": "S4", "score": 85},
                {"sprint": "S5", "score": 87}, {"sprint": "S6", "score": 87},
            ],
            "rejectionRate": 4, "blockerInvolvement": 0,
            "behaviourNotes": "Consistently high quality. Zero blocker involvement. Strong QA ownership.",
            "workloadHistory": [
                {"sprint": "S1", "load": 55}, {"sprint": "S2", "load": 58},
                {"sprint": "S3", "load": 60}, {"sprint": "S4", "load": 60},
                {"sprint": "S5", "load": 60}, {"sprint": "S6", "load": 60},
            ],
        },
        {
            "id": 5, "name": "Karan Joshi", "role": "Developer", "avatar": "KJ",
            "activeStories": 1, "alignmentAvg": 58, "risk": "High", "workload": 45,
            "status": "Active", "behaviourScore": 6.2,
            "sprintStories": [
                {"id": "ST-107", "title": "Notification Service", "points": 8, "status": "Blocked", "alignment": 42},
            ],
            "alignmentHistory": [
                {"sprint": "S1", "score": 68}, {"sprint": "S2", "score": 65},
                {"sprint": "S3", "score": 62}, {"sprint": "S4", "score": 60},
                {"sprint": "S5", "score": 58}, {"sprint": "S6", "score": 58},
            ],
            "rejectionRate": 22, "blockerInvolvement": 2,
            "behaviourNotes": "3 consecutive sprints below 60% alignment. Requires 1:1 coaching and closer story scoping.",
            "workloadHistory": [
                {"sprint": "S1", "load": 55}, {"sprint": "S2", "load": 50},
                {"sprint": "S3", "load": 48}, {"sprint": "S4", "load": 46},
                {"sprint": "S5", "load": 45}, {"sprint": "S6", "load": 45},
            ],
        },
    ]
    await db.team_members_detail.insert_many(team_members_detail)
    print(f"✅  Seeded {len(team_members_detail)} team member detail records")

    # ── SMReviewQueue.jsx ───────────────────────────────────────────────────────
    # id, story, developer, alignment, risk, submittedAt, status, aiNote
    review_queue_items = [
        {"id": "ST-103", "story": "User Profile API", "developer": "Vikram Singh", "alignment": 88, "risk": "Low", "submittedAt": "2h ago", "status": "Pending", "aiNote": "Alignment 88% — Code matches scope. Minor documentation gaps detected."},
        {"id": "ST-102", "story": "Setup CI/CD Pipeline", "developer": "Ananya Reddy", "alignment": 78, "risk": "High", "submittedAt": "4h ago", "status": "Pending", "aiNote": "Alignment 78% — Possible DevOps scope drift detected. Review pipeline configuration against sprint spec."},
        {"id": "ST-104", "story": "Dashboard UI Redesign", "developer": "Rahul Verma", "alignment": 65, "risk": "High", "submittedAt": "6h ago", "status": "Changes Requested", "aiNote": "Alignment 42% — Significant scope drift. UI components do not match wireframe spec."},
        {"id": "ST-109", "story": "API Rate Limiting", "developer": "Vikram Singh", "alignment": 82, "risk": "Low", "submittedAt": "1d ago", "status": "Pending", "aiNote": "Alignment 82% — Looks aligned with sprint backlog. Edge case handling could be improved."},
        {"id": "ST-106", "story": "Database Migration Script", "developer": "Ananya Reddy", "alignment": 72, "risk": "Medium", "submittedAt": "1d ago", "status": "Escalated to PM", "aiNote": "Alignment 72% — Schema drift from original spec. PM review recommended before merge."},
        {"id": "ST-107", "story": "Notification Service", "developer": "Karan Joshi", "alignment": 58, "risk": "High", "submittedAt": "2d ago", "status": "Rejected", "aiNote": "Alignment 42% — Possible scope drift detected. Implementation does not match story criteria."},
    ]
    await db.review_queue_items.insert_many(review_queue_items)
    print(f"✅  Seeded {len(review_queue_items)} review queue items")

    # ── SMRiskBlockers.jsx ─────────────────────────────────────────────────────
    # id, story, title, blockerType, owner, daysBlocked, risk, resolved
    blockers = [
        {"id": "B-01", "story": "ST-107", "title": "Notification Service", "blockerType": "Rejection Loop", "owner": "Karan Joshi", "daysBlocked": 5, "risk": "High", "resolved": False},
        {"id": "B-02", "story": "ST-102", "title": "Setup CI/CD Pipeline", "blockerType": "DevOps Failure", "owner": "Ananya Reddy", "daysBlocked": 2, "risk": "High", "resolved": False},
        {"id": "B-03", "story": "ST-104", "title": "Dashboard UI Redesign", "blockerType": "Scope Drift", "owner": "Rahul Verma", "daysBlocked": 3, "risk": "High", "resolved": False},
        {"id": "B-04", "story": "ST-106", "title": "Database Migration Script", "blockerType": "Approval Delay", "owner": "Ananya Reddy", "daysBlocked": 1, "risk": "Medium", "resolved": False},
        {"id": "B-05", "story": "ST-110", "title": "Monitoring Dashboard", "blockerType": "Overload", "owner": "Ananya Reddy", "daysBlocked": 0, "risk": "Medium", "resolved": True},
        {"id": "B-06", "story": "ST-103", "title": "User Profile API", "blockerType": "Approval Delay", "owner": "Vikram Singh", "daysBlocked": 0, "risk": "Low", "resolved": True},
    ]
    await db.blockers.insert_many(blockers)
    print(f"✅  Seeded {len(blockers)} blockers")

    # ── SMTeamPerformance.jsx ───────────────────────────────────────────────────
    # memberPerf: name, completion, alignmentAvg, reviewDelayAvg, rejectionRate, behaviourScore
    member_perf = [
        {"id": "mp-1", "name": "Vikram Singh", "completion": 94, "alignmentAvg": 91, "reviewDelayAvg": "1.2d", "rejectionRate": 5, "behaviourScore": 8.5},
        {"id": "mp-2", "name": "Ananya Reddy", "completion": 72, "alignmentAvg": 73, "reviewDelayAvg": "3.1d", "rejectionRate": 15, "behaviourScore": 7.5},
        {"id": "mp-3", "name": "Rahul Verma", "completion": 65, "alignmentAvg": 65, "reviewDelayAvg": "2.8d", "rejectionRate": 18, "behaviourScore": 6.8},
        {"id": "mp-4", "name": "Meera Nair", "completion": 96, "alignmentAvg": 87, "reviewDelayAvg": "0.8d", "rejectionRate": 4, "behaviourScore": 9.0},
        {"id": "mp-5", "name": "Karan Joshi", "completion": 48, "alignmentAvg": 58, "reviewDelayAvg": "4.5d", "rejectionRate": 22, "behaviourScore": 6.2},
    ]
    await db.member_perf.insert_many(member_perf)
    print(f"✅  Seeded {len(member_perf)} member performance records")

    # sprintTrend: sprint, completion, alignment, rejection
    sprint_trend = [
        {"id": "st-1", "sprint": "S1", "completion": 70, "alignment": 74, "rejection": 14},
        {"id": "st-2", "sprint": "S2", "completion": 74, "alignment": 76, "rejection": 13},
        {"id": "st-3", "sprint": "S3", "completion": 76, "alignment": 78, "rejection": 11},
        {"id": "st-4", "sprint": "S4", "completion": 78, "alignment": 75, "rejection": 10},
        {"id": "st-5", "sprint": "S5", "completion": 80, "alignment": 79, "rejection": 9},
        {"id": "st-6", "sprint": "S6", "completion": 82, "alignment": 80, "rejection": 8},
    ]
    await db.sprint_trend.insert_many(sprint_trend)
    print(f"✅  Seeded {len(sprint_trend)} sprint trend entries")

    # ── SMWorkload.jsx ─────────────────────────────────────────────────────────
    # workloadData: name, stories, points, reviewLoad, capacity
    sm_workload = [
        {"id": "wl-1", "name": "Vikram Singh", "stories": 3, "points": 17, "reviewLoad": 2, "capacity": 72},
        {"id": "wl-2", "name": "Ananya Reddy", "stories": 3, "points": 18, "reviewLoad": 1, "capacity": 92},
        {"id": "wl-3", "name": "Rahul Verma", "stories": 2, "points": 13, "reviewLoad": 1, "capacity": 58},
        {"id": "wl-4", "name": "Meera Nair", "stories": 2, "points": 10, "reviewLoad": 0, "capacity": 60},
        {"id": "wl-5", "name": "Karan Joshi", "stories": 1, "points": 8, "reviewLoad": 0, "capacity": 45},
    ]
    await db.sm_workload.insert_many(sm_workload)
    print(f"✅  Seeded {len(sm_workload)} SM workload entries")

    # suggestions: member, capacity, suggestion
    workload_suggestions = [
        {"id": "ws-1", "member": "Ananya Reddy", "capacity": 92, "suggestion": "Redistribute 2 stories to Rahul Verma or Karan Joshi"},
    ]
    await db.workload_suggestions.insert_many(workload_suggestions)
    print(f"✅  Seeded {len(workload_suggestions)} workload suggestions")

    print("\n🎉  All collections seeded successfully!")
    client.close()




if __name__ == "__main__":
    asyncio.run(seed())

