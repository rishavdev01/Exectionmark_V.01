"""
Employees route — CRUD (maps to employeeData.js + HREmployees/EmployeeProfile)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import employees_collection

router = APIRouter()




@router.get("")
async def get_employees():
    employees = []
    async for e in employees_collection.find({}, {"_id": 0}):
        employees.append(e)
    return employees


@router.get("/{emp_id}")
async def get_employee(emp_id: str):
    emp = await employees_collection.find_one({"id": emp_id}, {"_id": 0})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.post("")
async def create_employee(body: dict):
    body.pop("_id", None)
    await employees_collection.insert_one(body)
    return {"message": "Employee created"}


@router.put("/{emp_id}")
async def update_employee(emp_id: str, body: dict):
    result = await employees_collection.update_one({"id": emp_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated"}
