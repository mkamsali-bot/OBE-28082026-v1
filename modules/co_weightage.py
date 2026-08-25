import re
from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.co_weightage_service import (
    course_weightages_exist,
    delete_weightages,
    generate_default_equal_weightages,
    get_all_cos,
    get_all_courses,
    get_assessment_pattern,
    get_course,
    get_course_assessment_components,
    get_course_type,
    get_weightage_mode,
    get_weightages,
    initialize_weightages,
    save_weightage,
    set_weightage_mode,
    update_weightage,
    validate_weightages,
    weightage_exists,
)

from services.co_weightage_service import (
    get_course_assessment
)
from services.co_weightage_service import get_assessment_components
router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ==========================================================
# CO Weightage Home
# ==========================================================

@router.get("/co-weightage")
def co_weightage(
    request: Request,
    course_id: Optional[int] = None,
    error: Optional[str] = None
):
    courses = get_all_courses()
    selected_course = None
    course_type = None
    cos = []
    weightages = []
    weightage_lookup = {}
    weightage_mode = "DEFAULT"
    assessment_components = []

    if course_id:
        selected_course = get_course(course_id)
        course_type = get_course_type(course_id)
        assessment_components = get_course_assessment_components(course_id)
        initialize_weightages(course_id)
        cos = get_all_cos(course_id)
        weightages = get_weightages(course_id)

        for row in weightages:
            weightage_lookup[row["co_id"]] = row

        weightage_mode = get_weightage_mode(course_id)
    assessment_structure = get_assessment_components(course_type)
    return templates.TemplateResponse(
        request=request,
        name="co_weightage.html",
        context={
            "title": "CO Weightage",
            "courses": courses,
            "selected_course": selected_course,
            "course_type": course_type,
            "assessment_components": assessment_components,
            "assessment_structure": assessment_structure,
            "cos": cos,
            "weightages": weightages,
            "weightage_lookup": weightage_lookup,
            "weightage_mode": weightage_mode,
            "error": error,
        },
    )

# ==========================================================
# Save CO Weightages
# ==========================================================

# Pattern to capture dynamic keys like: weightage[<co_id>][<component>]
import re
WEIGHTAGE_KEY_PATTERN = re.compile(
    r"weightage\[(\d+)\]\[(.+)\]"
)
@router.post("/co-weightage/save")
async def save_co_weightages(request: Request):

    form = await request.form()

    try:
        course_id = int(form.get("course_id", 0))
    except (ValueError, TypeError):
        course_id = 0
    weightage_mode = str(form.get("weightage_mode", "DEFAULT"))

    # 2. Extract dynamic weightage inputs from form
    # Structure: { co_id: { component_name: value } }
    parsed_weightages = {}

    for key, value in form.items():
        match = WEIGHTAGE_KEY_PATTERN.match(key)
        if not match:
            continue

        co_id = int(match.group(1))
        component = match.group(2)

        if co_id not in parsed_weightages:
            parsed_weightages[co_id] = {}

        try:
            parsed_weightages[co_id][component] = float(value or 0)
        except ValueError:
            parsed_weightages[co_id][component] = 0.0
    
    # 3. Validate inputs
    if not course_id or not parsed_weightages:
        return RedirectResponse(
            url="/co-weightage?error=missing_data",
            status_code=303
        )

    course_type = get_course_type(course_id)
    
    weightages_list = list(parsed_weightages.values())
    
    if not validate_weightages(course_type, weightages_list):
        return RedirectResponse(
            url=f"/co-weightage?course_id={course_id}&error=validation_failed",
            status_code=303
        )

    
    # 4. Save to Database
    delete_weightages(course_id)

    for co_id, components in parsed_weightages.items():

        
        save_weightage(
            course_id=course_id,
            co_id=co_id,
            weightage_mode=weightage_mode,
            le=components.get("LE", 0.0),
            se1=components.get("SE1", 0.0),
            se2=components.get("SE2", 0.0),
            mid1=components.get("MID1", 0.0),
            mid2=components.get("MID2", 0.0),
            record=components.get("Record", 0.0),
            evaluation=components.get("Evaluation", 0.0),
        )

    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )
# ==========================================================
# Load Selected Course
# ==========================================================

@router.get("/co-weightage/course")
def load_course(course_id: int):
    initialize_weightages(course_id)
    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )


# ==========================================================
# Generate Default Equal Weightages
# ==========================================================

@router.post("/co-weightage/default")
def generate_default(course_id: int = Form(...)):
    generate_default_equal_weightages(course_id)
    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )


# ==========================================================
# Change Weightage Mode
# ==========================================================

@router.post("/co-weightage/mode")
def change_weightage_mode(
    course_id: int = Form(...),
    weightage_mode: str = Form(...)
):
    set_weightage_mode(course_id, weightage_mode)
    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )


# ==========================================================
# Delete All Weightages of Selected Course
# ==========================================================

@router.get("/co-weightage/delete/{course_id}")
def delete_course_weightages(course_id: int):
    delete_weightages(course_id)
    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )


# ==========================================================
# Refresh Selected Course
# ==========================================================

@router.get("/co-weightage/refresh/{course_id}")
def refresh_course(course_id: int):
    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )


# ==========================================================
# Reload Default Weightages
# ==========================================================

@router.get("/co-weightage/reset/{course_id}")
def reset_default_weightages(course_id: int):
    delete_weightages(course_id)
    generate_default_equal_weightages(course_id)
    return RedirectResponse(
        url=f"/co-weightage?course_id={course_id}",
        status_code=303
    )


# ==========================================================
# Get Course Type (AJAX)
# ==========================================================

@router.get("/co-weightage/course-type/{course_id}")
def get_course_type_endpoint(course_id: int):
    return {"course_type": get_course_type(course_id)}


# ==========================================================
# Assessment Pattern (AJAX)
# ==========================================================

@router.get("/co-weightage/pattern/{course_id}")
def assessment_pattern(course_id: int):
    course_type_val = get_course_type(course_id)
    pattern = get_assessment_pattern(course_type_val)
    return {
        "course_type": course_type_val,
        "pattern": pattern
    }


# ==========================================================
# Check Whether Weightages Exist
# ==========================================================

@router.get("/co-weightage/status/{course_id}")
def weightage_status(course_id: int):
    return {
        "exists": course_weightages_exist(course_id),
        "mode": get_weightage_mode(course_id)
    }

@router.get("/co-weightage/course/{course_id}")
def course_assessment(course_id: int):

    return get_course_assessment(course_id)