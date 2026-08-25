from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from services.co_po_service import (
    get_all_mappings,
    get_mapping,
    mapping_exists,
    add_mapping,
    update_mapping,
    delete_mapping
)

from services.course_service import get_all_courses
from services.co_service import get_all_cos

router = APIRouter()

templates = Jinja2Templates(directory="templates")


# ==========================================================
# CO-PO Mapping Home
# ==========================================================
@router.get("/co-mapping")
def co_mapping(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="co_po.html",
        context={
            "mappings": get_all_mappings(),
            "courses": get_all_courses(),
            "cos": get_all_cos(),
            "mapping": None
        }
    )


# ==========================================================
# Save Mapping
# ==========================================================
@router.post("/co-po/save")
def save_mapping(

    course_id: int = Form(...),
    co_id: int = Form(...),

    po1: int = Form(0),
    po2: int = Form(0),
    po3: int = Form(0),
    po4: int = Form(0),
    po5: int = Form(0),
    po6: int = Form(0),
    po7: int = Form(0),
    po8: int = Form(0),
    po9: int = Form(0),
    po10: int = Form(0),
    po11: int = Form(0),
    po12: int = Form(0),

    pso1: int = Form(0),
    pso2: int = Form(0),
    pso3: int = Form(0),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    if not mapping_exists(course_id, co_id):

        add_mapping(

            course_id,
            co_id,

            po1,
            po2,
            po3,
            po4,
            po5,
            po6,
            po7,
            po8,
            po9,
            po10,
            po11,
            po12,

            pso1,
            pso2,
            pso3,

            active

        )

    return RedirectResponse(
    url="/co-mapping",
    status_code=303
)
# ==========================================================
# Edit Mapping
# ==========================================================
@router.get("/co-po/edit/{mapping_id}")
def edit_mapping(mapping_id: int, request: Request):

    return templates.TemplateResponse(
        request=request,
        name="co_po.html",
        context={
            "mappings": get_all_mappings(),
            "courses": get_all_courses(),
            "cos": get_all_cos(),
            "mapping": get_mapping(mapping_id)
        }
    )


# ==========================================================
# Update Mapping
# ==========================================================
@router.post("/co-po/update/{mapping_id}")
def update_mapping_record(

    mapping_id: int,

    course_id: int = Form(...),
    co_id: int = Form(...),

    po1: int = Form(0),
    po2: int = Form(0),
    po3: int = Form(0),
    po4: int = Form(0),
    po5: int = Form(0),
    po6: int = Form(0),
    po7: int = Form(0),
    po8: int = Form(0),
    po9: int = Form(0),
    po10: int = Form(0),
    po11: int = Form(0),
    po12: int = Form(0),

    pso1: int = Form(0),
    pso2: int = Form(0),
    pso3: int = Form(0),

    is_active: Optional[int] = Form(None)

):

    active = 1 if is_active else 0

    update_mapping(

        mapping_id,

        course_id,
        co_id,

        po1,
        po2,
        po3,
        po4,
        po5,
        po6,
        po7,
        po8,
        po9,
        po10,
        po11,
        po12,

        pso1,
        pso2,
        pso3,

        active

    )

    return RedirectResponse(
        url="/co-mapping",
        status_code=303
    )


# ==========================================================
# Delete Mapping
# ==========================================================
@router.get("/co-po/delete/{mapping_id}")
def delete_mapping_record(mapping_id: int):

    delete_mapping(mapping_id)

    return RedirectResponse(
        url="/co-mapping",
        status_code=303
    )