import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def create_users():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    lead = {
        "id": "EMPLEAD001",
        "password": "emplead@123",
        "name": "Sneha Iyer",
        "role": "LEAD",
        "email": "sneha@exactiomark.com",
        "department": "Engineering",
        "avatar": "SI",
        "phone": "+91 98765 43210",
        "github_pat": "",
    }

    dev = {
        "id": "EMPDEV001",
        "password": "empdev@123",
        "name": "Vikram Singh",
        "role": "DEVELOPER",
        "email": "vikram@exactiomark.com",
        "department": "Engineering",
        "avatar": "VS",
        "phone": "+91 98765 43211",
        "github_pat": "",
    }

    # Remove any existing users with the same email or ID (to avoid duplicates)
    for u in [lead, dev]:
        await db.users.delete_many({"$or": [{"email": u["email"]}, {"id": u["id"]}]})
        await db.employees.delete_many({"$or": [{"email": u["email"]}, {"id": u["id"]}]})

    # Insert into users collection
    await db.users.insert_many([lead, dev])
    
    # Insert into employees collection (minimal version for registration)
    lead_emp = {**lead, "dept": lead["department"], "projects": ["Sprint Alpha"], "status": "Active", "perfScore": 86.8, "behaviour": 9.0, "risk": "Low", "sprintContrib": "18 SP", "alignment": 87, "onTime": 88, "rejection": 8, "alignmentHistory": [], "sprintTrend": [], "behaviourScores": {"communication": 9, "ownership": 8, "teamwork": 9, "leadership": 8, "discipline": 9}, "managerComment": "Great facilitator.", "riskData": {"overloadFreq": 0, "escalationInvolvement": 0, "perfDrop": 0}, "promotion": {"eligible": True, "aiVerdict": "Recommend", "managerReview": "Pending", "finalDecision": "—", "lastReview": "—", "reviewedBy": "—"}, "sprintTasks": 5, "workload": 65}
    dev_emp = {**dev, "dept": dev["department"], "projects": ["Sprint Alpha", "Sprint Beta"], "status": "Active", "perfScore": 89.2, "behaviour": 8.5, "risk": "Low", "sprintContrib": "24 SP", "alignment": 91, "onTime": 94, "rejection": 5, "alignmentHistory": [], "sprintTrend": [], "behaviourScores": {"communication": 9, "ownership": 9, "teamwork": 8, "leadership": 7, "discipline": 9}, "managerComment": "Consistently delivers high-quality code.", "riskData": {"overloadFreq": 2, "escalationInvolvement": 1, "perfDrop": -3.2}, "promotion": {"eligible": True, "aiVerdict": "Strongly Recommend", "managerReview": "Approved", "finalDecision": "Promoted", "lastReview": "Feb 15, 2026", "reviewedBy": "Priya Sharma"}, "sprintTasks": 8, "workload": 72}
    
    await db.employees.insert_many([lead_emp, dev_emp])

    print(f"✅ Created 2 users and matching employee profiles\n")
    print(f"LEAD: {lead['id']} / {lead['password']}")
    print(f"DEV: {dev['id']} / {dev['password']}")

if __name__ == "__main__":
    asyncio.run(create_users())
