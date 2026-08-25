import threading
import time
import webbrowser
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize database
from database import initialize_database

# Routers
from modules.department import router as department_router
from modules.faculty import router as faculty_router
from modules.course import router as course_router
from modules.po import router as po_router
from modules.pso import router as pso_router
from modules.co import router as co_router
from modules.co_po import router as co_po_router
from modules.program import router as program_router
from modules.co_weightage import router as co_weightage_router
from services.co_service import get_cos_by_course
from modules.marks_upload import router as marks_upload_router
from modules.co_attainment import router as co_attainment_router
from fastapi.responses import FileResponse
from modules import co_weightage
from services.course_service import get_all_courses
from modules.indirect_attainment import router as indirect_attainment_router
from modules.nba_reports import router as nba_reports_router

# ---------------------------------------------------------
# Database & FastAPI App Initialization
# ---------------------------------------------------------
initialize_database()
app = FastAPI(title="OBE Analytics Pro")

# Static Files & Templates
#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(department_router)
app.include_router(faculty_router)
app.include_router(course_router)
app.include_router(po_router)
app.include_router(pso_router)
app.include_router(co_router)
app.include_router(co_po_router)
app.include_router(program_router)
app.include_router(co_weightage_router)
app.include_router(marks_upload_router)
app.include_router(co_attainment_router)
app.include_router(indirect_attainment_router)
app.include_router(nba_reports_router)

from fastapi.responses import FileResponse

app.include_router(course_router)
app.include_router(co_attainment_router)
app.include_router(co_po_router)
app.include_router(co_weightage.router)

# ---------------------------------------
# Attainment HTML Page
# ---------------------------------------
@app.get("/attainment")
def course_attainment_page(request: Request):

    courses = get_all_courses()

    return templates.TemplateResponse(
        request=request,
        name="attainment.html",
        context={
            "title": "Course Attainment",
            "courses": courses
        }
    )
# ---------------------------------------------------------
# Page Routes
# ---------------------------------------------------------
@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"title": "Dashboard"}
    )


@app.get("/masters")
def masters(request: Request):
    return templates.TemplateResponse(
        request=request, name="masters.html", context={"title": "Masters"}
    )


@app.get("/assessment")
def assessment(request: Request):
    return templates.TemplateResponse(
        request=request, name="assessment.html", context={"title": "Assessment"}
    )


@app.get("/reports")
def reports(request: Request):
    return templates.TemplateResponse(
        request=request, name="reports.html", context={"title": "Reports"}
    )


# ---------------------------------------------------------
# Browser Auto-Open Helper
# ---------------------------------------------------------
def open_browser():
    """Waits for server initialization before opening browser."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")


# ---------------------------------------------------------
# Run Application
# ---------------------------------------------------------
if __name__ == "__main__":

    # Spawn browser thread once before Uvicorn takes over main thread
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )