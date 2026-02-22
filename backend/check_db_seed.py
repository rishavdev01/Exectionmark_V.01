import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_seed():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.exactionmark
    count = await db.performance_members.count_documents({})
    print(f"Total performance members: {count}")
    
    if count > 0:
        member = await db.performance_members.find_one({})
        print(f"Sample member keys: {list(member.keys())}")
        if 'sprintContrib' in member:
            print("✅ 'sprintContrib' field found in database.")
        else:
            print("❌ 'sprintContrib' field NOT found. Seed might be outdated or not run.")
    else:
        print("❌ No members found in performance_members collection.")

if __name__ == "__main__":
    asyncio.run(check_seed())
