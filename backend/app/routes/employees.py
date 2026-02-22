"""
Employees route — CRUD (maps to employeeData.js + HREmployees/EmployeeProfile)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import employees_collection

router = APIRouter()


class EmployeeCreate(BaseModel):
    id: int
    name: str
    role: str
    avatar: str
    department: str
    status: str = "Active"
    risk: str = "Low"
    alignment: int = 0
    onTime: int = 0
    rejection: int = 0
    behaviour: float = 0.0
    joinDate: str = ""
    sprintTasks: int = 0
    workload: int = 0


@router.get("")
async def get_employees():
    employees = []
    async for e in employees_collection.find({}, {"_id": 0}):
        employees.append(e)
    return employees


@router.get("/{emp_id}")
async def get_employee(emp_id: int):
    emp = await employees_collection.find_one({"id": emp_id}, {"_id": 0})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.post("")
async def create_employee(body: EmployeeCreate):
    await employees_collection.insert_one(body.model_dump())
    return {"message": "Employee created"}


@router.put("/{emp_id}")
async def update_employee(emp_id: int, body: dict):
    result = await employees_collection.update_one({"id": emp_id}, {"$set": body})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated"}
