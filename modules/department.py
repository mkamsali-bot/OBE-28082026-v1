from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.department_service import (
    get_all_departments,
    get_department,
    department_exists,
    add_department,
    update_department,
    delete_department,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# --------------------------------------------------------
# Department Home
# --------------------------------------------------------
@router.get("/department")
def department(request: Request):

    departments = get_all_departments()

    return templates.TemplateResponse(
        request=request,
        name="department.html",
        context={
            "title": "Department",
            "department": None,
            "departments": departments
        }
    )


# --------------------------------------------------------
# Save Department
# --------------------------------------------------------
@router.post("/department/save")
def save_department(
    department_code: str = Form(...),
    department_name: str = Form(...),
    is_active: Optional[int] = Form(None)
):

    active = 1 if is_active else 0

    if not department_exists(department_code):

        add_department(
            department_code,
            department_name,
            active
        )

    return RedirectResponse(
        url="/department",
        status_code=303
    )


# --------------------------------------------------------
# Edit Department
# --------------------------------------------------------
@router.get("/department/edit/{id}")
def edit_department(request: Request, id: int):

    departments = get_all_departments()

    department = get_department(id)

    return templates.TemplateResponse(
        request=request,
        name="department.html",
        context={
            "title": "Department",
            "department": department,
            "departments": departments
        }
    )


# --------------------------------------------------------
# Update Department
# --------------------------------------------------------
@router.post("/department/update/{id}")
def update_department_route(
    id: int,
    department_code: str = Form(...),
    department_name: str = Form(...),
    is_active: Optional[int] = Form(None)
):

    active = 1 if is_active else 0

    update_department(
        id,
        department_code,
        department_name,
        active
    )

    return RedirectResponse(
        url="/department",
        status_code=303
    )


# --------------------------------------------------------
# Delete Department (Soft Delete)
# --------------------------------------------------------
@router.get("/department/delete/{id}")
def delete_department_route(id: int):

    delete_department(id)

    return RedirectResponse(
        url="/department",
        status_code=303
    )