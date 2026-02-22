from fastapi import APIRouter, HTTPException
from typing import Optional
from app.database import user_logins_collection
from app.models.user_login import UserLogin

router = APIRouter()


@router.get("", response_model=list[UserLogin])
async def get_user_logins():
    return [doc async for doc in user_logins_collection.find({}, {"_id": 0})]


@router.get("/{employee_id}", response_model=UserLogin)
async def get_user_login(employee_id: str):
    doc = await user_logins_collection.find_one({"employee_id": employee_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="User login not found")
    return doc


@router.post("", response_model=dict)
async def create_user_login(body: UserLogin):
    existing = await user_logins_collection.find_one({"employee_id": body.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    await user_logins_collection.insert_one(body.model_dump())
    return {"message": "User login created"}


@router.put("/{employee_id}", response_model=dict)
async def update_user_login(employee_id: str, body: dict):
    body.pop("_id", None)
    result = await user_logins_collection.update_one(
        {"employee_id": employee_id}, {"$set": body}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Updated"}
