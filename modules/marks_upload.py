import io
from io import BytesIO
from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from services.course_service import get_all_courses, get_course
from services.co_weightage_service import get_course_type
from services.marks_excel_service import (
    get_assessment_components,
    generate_marks_template,
    read_marks_excel,
    validate_marks_data,
    prepare_marks_for_import,
    import_marks,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ==========================================================
# Step 1: Marks Home
# ==========================================================

@router.get("/marks", response_class=HTMLResponse)
def marks_upload(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="marks_upload.html",
        context={
            "title": "Marks Upload",
            "courses": get_all_courses(),
            "selected_course": None,
            "course_type": None,
            "components": [],
            "validation": None,
            "message": None,
        },
    )


# ==========================================================
# Step 2: Select Course
# ==========================================================

@router.get("/marks/course", response_class=HTMLResponse)
def load_course(request: Request, course_id: int):
    courses = get_all_courses()
    selected_course = get_course(course_id) if callable(get_course) else next(
        (c for c in courses if c["id"] == course_id), None
    )

    if not selected_course:
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": None,
                "course_type": None,
                "components": [],
                "validation": None,
                "message": "Course not found.",
            },
        )

    course_type = get_course_type(course_id)
    components = get_assessment_components(course_type)

    return templates.TemplateResponse(
        request=request,
        name="marks_upload.html",
        context={
            "title": "Marks Upload",
            "courses": courses,
            "selected_course": selected_course,
            "course_type": course_type,
            "components": components,
            "validation": None,
            "message": None,
        },
    )


# ==========================================================
# Step 3: Download Excel Template
# ==========================================================

@router.get("/marks/template")
def download_marks_template(course_id: int):
    courses = get_all_courses()
    selected_course = get_course(course_id) if callable(get_course) else next(
        (c for c in courses if c["id"] == course_id), None
    )

    if not selected_course:
        return RedirectResponse(url="/marks", status_code=303)

    course_type = get_course_type(course_id)
    
    excel_data = generate_marks_template(course_type)

    course_code = str(selected_course["course_code"]).strip().replace(" ", "_")
    filename = f"{course_code}_Marks_Template.xlsx"

    return StreamingResponse(
        BytesIO(excel_data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ==========================================================
# Step 4: Validate Uploaded Excel File
# ==========================================================

@router.post("/marks/validate")
async def validate_marks_upload(
    request: Request,
    course_id: int = Form(...),
    file: UploadFile = File(...),
):
    courses = get_all_courses()
    selected_course = get_course(course_id) if callable(get_course) else next(
        (c for c in courses if c["id"] == course_id), None
    )

    if not selected_course:
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": None,
                "course_type": None,
                "components": [],
                "validation": None,
                "message": "Course not found.",
            },
        )

    if not file.filename:
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": selected_course,
                "course_type": None,
                "components": [],
                "validation": None,
                "message": "Please select an Excel file.",
            },
        )

    if not file.filename.lower().endswith((".xlsx", ".xls")):
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": selected_course,
                "course_type": None,
                "components": [],
                "validation": None,
                "message": "Only Excel files (.xlsx, .xls) are allowed.",
            },
        )

    course_type = get_course_type(course_id)
    components = get_assessment_components(course_type)

    file_bytes = await file.read()
    excel_result = read_marks_excel(file_bytes=file_bytes, course_type=course_type)

    if not excel_result["success"]:
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": selected_course,
                "course_type": course_type,
                "components": components,
                "validation": None,
                "message": excel_result["error"],
            },
        )

    validation = validate_marks_data(
        df=excel_result["data"], course_type=course_type
    )
    import_rows = prepare_marks_for_import(
        validation_result=validation,
        course_id=course_id,
        course_type=course_type,
    )

    return templates.TemplateResponse(
        request=request,
        name="marks_upload.html",
        context={
            "title": "Marks Upload",
            "courses": courses,
            "selected_course": selected_course,
            "course_type": course_type,
            "components": components,
            "validation": validation,
            "import_rows": import_rows,
            "filename": file.filename,
            "message": None,
        },
    )


# ==========================================================
# Step 5: Import Marks to Database
# ==========================================================

@router.post("/marks/import")
async def import_marks_upload(
    request: Request,
    course_id: int = Form(...),
    file: UploadFile = File(...),
):
    courses = get_all_courses()
    selected_course = get_course(course_id) if callable(get_course) else next(
        (c for c in courses if c["id"] == course_id), None
    )

    if not selected_course:
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": None,
                "course_type": None,
                "components": [],
                "validation": None,
                "message": "Course not found.",
            },
        )

    if not file.filename or not file.filename.lower().endswith((".xlsx", ".xls")):
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": selected_course,
                "course_type": None,
                "components": [],
                "validation": None,
                "message": "Please select a valid Excel file.",
            },
        )

    course_type = get_course_type(course_id)
    components = get_assessment_components(course_type)

    file_bytes = await file.read()
    excel_result = read_marks_excel(file_bytes=file_bytes, course_type=course_type)

    if not excel_result["success"]:
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": selected_course,
                "course_type": course_type,
                "components": components,
                "validation": None,
                "message": excel_result["error"],
            },
        )

    validation = validate_marks_data(
        df=excel_result["data"], course_type=course_type
    )

    if not validation.get("valid", False):
        return templates.TemplateResponse(
            request=request,
            name="marks_upload.html",
            context={
                "title": "Marks Upload",
                "courses": courses,
                "selected_course": selected_course,
                "course_type": course_type,
                "components": components,
                "validation": validation,
                "filename": file.filename,
                "message": "Marks were not imported. Please correct the Excel errors.",
            },
        )

    import_rows = prepare_marks_for_import(
        validation_result=validation,
        course_id=course_id,
        course_type=course_type,
    )

    result = import_marks(
    import_rows=import_rows,
    course_id=course_id,
    course_type=course_type,
)

    return templates.TemplateResponse(
        request=request,
        name="marks_upload.html",
        context={
            "title": "Marks Upload",
            "courses": courses,
            "selected_course": selected_course,
            "course_type": course_type,
            "components": components,
            "validation": validation,
            "filename": file.filename,
            "message": result.get("message"),
            "imported": result.get("success", False),
            "total_imported": result.get("imported", 0),
        },
    )