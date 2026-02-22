"""
Companies route — CRUD, backend-only seeding.
Passwords are excluded from GET responses.
"""

from fastapi import APIRouter, HTTPException
from app.database import companies_collection
from app.models.company_models import Company, CompanyOut

router = APIRouter()


@router.get("", response_model=list[CompanyOut])
async def get_companies():
    """Return all companies (passwords excluded)."""
    return [doc async for doc in companies_collection.find({}, {"_id": 0, "org_password": 0, "admin_password": 0})]


@router.get("/{company_id}", response_model=CompanyOut)
async def get_company(company_id: str):
    doc = await companies_collection.find_one({"company_id": company_id}, {"_id": 0, "org_password": 0, "admin_password": 0})
    if not doc:
        raise HTTPException(404, "Company not found")
    return doc


@router.post("", response_model=dict)
async def create_company(body: Company):
    existing = await companies_collection.find_one({"company_id": body.company_id})
    if existing:
        raise HTTPException(400, "Company ID already exists")
    await companies_collection.insert_one(body.model_dump())
    return {"message": "Company created"}


@router.put("/{company_id}", response_model=dict)
async def update_company(company_id: str, body: dict):
    body.pop("_id", None)
    result = await companies_collection.update_one({"company_id": company_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(404, "Company not found")
    return {"message": "Company updated"}


@router.delete("/{company_id}", response_model=dict)
async def delete_company(company_id: str):
    result = await companies_collection.delete_one({"company_id": company_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Company not found")
    return {"message": "Company deleted"}
