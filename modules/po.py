from typing import Optional

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.po_service import (
    get_all_pos,
    get_po,
    po_exists,
    add_po,
    update_po,
    delete_po,
    load_default_pos
)

from services.department_service import get_all_departments

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# Program Outcome Home
# ==========================================================
@router.get("/po")
def po(request: Request):

    pos = get_all_pos()
    departments = get_all_departments()

    return templates.TemplateResponse(
        request=request,
        name="po.html",
        context={
            "title": "Program Outcomes",
            "pos": pos,
            "departments": departments,
            "po": None
        }
    )


# ==========================================================
# Save PO
# ==========================================================
@router.post("/po/save")
def save_po(

    po_code: str = Form(...),
    po_description: str = Form(...),
    department_id: int = Form(...),
    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not po_exists(po_code, department_id):

        add_po(
            po_code,
            po_description,
            department_id,
            active
        )

    return RedirectResponse(
        url="/po",
        status_code=303
    )


# ==========================================================
# Edit PO
# ==========================================================
@router.get("/po/edit/{id}")
def edit_po(id: int, request: Request):

    po = get_po(id)

    pos = get_all_pos()

    departments = get_all_departments()

    return templates.TemplateResponse(
        request=request,
        name="po.html",
        context={
            "title": "Program Outcomes",
            "po": po,
            "pos": pos,
            "departments": departments
        }
    )


# ==========================================================
# Update PO
# ==========================================================
@router.post("/po/update/{id}")
def update_po_record(

    id: int,

    po_code: str = Form(...),
    po_description: str = Form(...),
    department_id: int = Form(...),
    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_po(

        id,
        po_code,
        po_description,
        department_id,
        active

    )

    return RedirectResponse(
        url="/po",
        status_code=303
    )


# ==========================================================
# Delete PO (Soft Delete)
# ==========================================================
@router.get("/po/delete/{id}")
def delete_po_record(id: int):

    delete_po(id)

    return RedirectResponse(
        url="/po",
        status_code=303
    )


# ==========================================================
# Load Default AICTE / NBA POs
# ==========================================================
@router.get("/po/load-default/{department_id}")
def load_default_po(department_id: int):

    load_default_pos(department_id)

    return RedirectResponse(
        url="/po",
        status_code=303
    )