"""
Seed script for companies collection.
Run: python seed_companies.py

This is backend-only — not exposed in frontend.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "exactionmark"

COMPANIES = [
    {
        "company_id": "COMP-001",
        "name": "Exactiomark Technologies",
        "org_password": "ExactOrg@2026",
        "admin": "admin@exactiomark.com",
        "admin_password": "Admin@Exact2026",
    },
    {
        "company_id": "COMP-002",
        "name": "NovaTech Solutions",
        "org_password": "NovaTech@2026",
        "admin": "admin@novatech.io",
        "admin_password": "Admin@Nova2026",
    },
    {
        "company_id": "COMP-003",
        "name": "AetherCloud Inc.",
        "org_password": "Aether@Cloud2026",
        "admin": "admin@aethercloud.com",
        "admin_password": "Admin@Aether2026",
    },
]


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    col = db["companies"]

    # Clear existing
    await col.delete_many({})

    # Insert
    await col.insert_many(COMPANIES)
    print(f"✅ Seeded {len(COMPANIES)} companies into '{DB_NAME}.companies'")

    # Verify
    count = await col.count_documents({})
    print(f"   Total documents: {count}")

    async for doc in col.find({}, {"_id": 0, "org_password": 0, "admin_password": 0}):
        print(f"   → {doc['company_id']}: {doc['name']} (admin: {doc['admin']})")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
