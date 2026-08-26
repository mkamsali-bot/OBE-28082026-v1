import sqlite3
from database import get_connection
# ==========================================================
# Convert SQLite Row to Dictionary
# ==========================================================

def row_to_dict(row):
    return dict(row)

import os



DB_NAME = "obe.db"

# ==========================================================
# Database Connection
# ==========================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ==========================================================
# Course Queries
# ==========================================================

def get_courses():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, course_code, course_name
            FROM Course
            WHERE is_active = 1
            ORDER BY course_code
        """)
        return [
            {
                "course_id": row["id"],
                "course_code": row["course_code"],
                "course_name": row["course_name"]
            }
            for row in cursor.fetchall()
        ]

def get_course_details(course_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, course_code, course_name, semester, credits,
                   regulation, course_type, department_id, program_id, faculty_id
            FROM Course
            WHERE id = ? AND is_active = 1
        """, (course_id,))
        row = cursor.fetchone()
        
        if not row:
            return None

        return {
            "course_id": row["id"],
            "course_code": row["course_code"],
            "course_name": row["course_name"],
            "semester": row["semester"],
            "credits": row["credits"],
            "regulation": row["regulation"],
            "course_type": row["course_type"],
            "department_id": row["department_id"],
            "program_id": row["program_id"],
            "faculty_id": row["faculty_id"]
        }

def get_all_courses():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, course_code, course_name, course_type
            FROM Course
            WHERE is_active = 1
            ORDER BY course_code
        """).fetchall()

def get_course(course_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT * FROM Course WHERE id = ?
        """, (course_id,)).fetchone()

def get_course_type(course_id):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT course_type FROM Course WHERE id = ?
        """, (course_id,)).fetchone()
        return row["course_type"] if row else None

# ==========================================================
# Course Outcome (CO) Queries
# ==========================================================

def get_all_cos(course_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, co_code, co_description
            FROM CourseOutcome
            WHERE course_id = ?
            AND is_active=1
            ORDER BY co_code
        """, (course_id,)).fetchall()

# Alias for backward compatibility if required elsewhere
get_course_cos = get_all_cos

# ==========================================================
# Assessment Components & Weightages
# ==========================================================

def get_course_assessment_components(course_id):
    course = get_course_details(course_id)

    if not course:
        return []

    course_type = course["course_type"]

    if course_type == "Theory":
        return ["LE", "SE1", "SE2"]

    elif course_type == "Theory + Practical":
        return [
            "LE",
            "SE1",
            "SE2",
            "MID1",
            "MID2",
            "Record"
        ]

    elif course_type in (
        "Project",
        "Capstone",
        "Capstone Project",
        "Internship"
    ):
        return ["Evaluation"]

    return []

def load_weightage(course_id):

    course = get_course_details(course_id)

    if not course:
        return None

    cos = get_all_cos(course_id)

    components = get_course_assessment_components(course_id)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT co_id, le_weightage, se1_weightage, se2_weightage,
                   mid1_weightage, mid2_weightage, record_weightage, evaluation_weightage
            FROM COWeightage
            WHERE course_id = ?
        """, (course_id,))
        weightage_rows = cursor.fetchall()

    weightage_lookup = {
        row["co_id"]: {
            "LE": row["le_weightage"] or 0,
            "SE1": row["se1_weightage"] or 0,
            "SE2": row["se2_weightage"] or 0,
            "MID1": row["mid1_weightage"] or 0,
            "MID2": row["mid2_weightage"] or 0,
            "Record": row["record_weightage"] or 0,
            "Evaluation": row["evaluation_weightage"] or 0
        }
        for row in weightage_rows
    }

    rows = []
    for co in cos:
        saved = weightage_lookup.get(co["id"], {})
        component_values = {comp: saved.get(comp, 0) for comp in components}

        rows.append({
            "co_id": co["id"],
            "co_code": co["co_code"],
            "description": co["co_description"],
            "weightages": component_values
        })

    return {
        "course": course,
        "components": components,
        "rows": rows
    }

def get_weightages(course_id):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM COWeightage
            WHERE course_id = ?
            ORDER BY co_id
        """, (course_id,)).fetchall()

    result = []

    for row in rows:
        item = dict(row)

        item["values"] = {
            "LE": item["le_weightage"] or 0,
            "SE1": item["se1_weightage"] or 0,
            "SE2": item["se2_weightage"] or 0,
            "MID1": item["mid1_weightage"] or 0,
            "MID2": item["mid2_weightage"] or 0,
            "Record": item["record_weightage"] or 0,
            "Evaluation": item["evaluation_weightage"] or 0
        }

        item["total"] = sum(item["values"].values())
        result.append(item)

    return result
def delete_weightages(course_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM COWeightage WHERE course_id = ?",
            (course_id,)
        )
        conn.commit()


def save_weightage(course_id, co_id, weightage_mode,
                   le, se1, se2, mid1, mid2, record, evaluation):

    with get_connection() as conn:

        print("Saving to database")
        print("Course ID :", course_id)
        print("CO ID     :", co_id)
        print("LE        :", le)
        print("SE1       :", se1)
        print("SE2       :", se2)
        print("MID1      :", mid1)
        print("MID2      :", mid2)
        print("Record    :", record)
        print("Evaluation:", evaluation)
        print("-" * 50)

        conn.execute("""
            INSERT INTO COWeightage (
                course_id,
                co_id,
                weightage_mode,
                le_weightage,
                se1_weightage,
                se2_weightage,
                mid1_weightage,
                mid2_weightage,
                record_weightage,
                evaluation_weightage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            course_id,
            co_id,
            weightage_mode,
            le,
            se1,
            se2,
            mid1,
            mid2,
            record,
            evaluation
        ))
        conn.commit()

        row = conn.execute("""
            SELECT
            le_weightage,
            se1_weightage,
            se2_weightage,
            mid1_weightage,
            mid2_weightage,
            record_weightage,
            evaluation_weightage
        FROM COWeightage
        WHERE course_id = ? AND co_id = ?
    """, (course_id, co_id)).fetchone()

    print("Saved row =", dict(row))
        
def update_weightage(course_id, co_id, weightage_mode, le, se1, se2, mid1, mid2, record, evaluation):
    with get_connection() as conn:
        conn.execute("""
            UPDATE COWeightage
            SET weightage_mode = ?,
                le_weightage = ?, se1_weightage = ?, se2_weightage = ?,
                mid1_weightage = ?, mid2_weightage = ?, record_weightage = ?,
                evaluation_weightage = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE course_id = ? AND co_id = ?
        """, (weightage_mode, le, se1, se2, mid1, mid2, record, evaluation, course_id, co_id))
        conn.commit()

def weightage_exists(course_id, co_id):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id FROM COWeightage WHERE course_id = ? AND co_id = ?
        """, (course_id, co_id)).fetchone()
        return row is not None

# ==========================================================
# Default Weightage Generation
# ==========================================================

def _distribute_equally(total, n):
    """Helper to distribute total integer weight evenly across n items with precision fix."""
    base = round(total / n, 2)
    return [base] * n

def generate_default_equal_weightages(course_id):
    course_type = get_course_type(course_id)
    cos = get_all_cos(course_id)
    n = len(cos)

    if n == 0:
        return

    delete_weightages(course_id)

    pattern = get_assessment_pattern(course_type)
    distributed = {key: _distribute_equally(val, n) for key, val in pattern.items()}

    for idx, co in enumerate(cos):
        save_weightage(
            course_id=course_id,
            co_id=co["id"],
            weightage_mode="DEFAULT",
            le=distributed.get("LE", [0]*n)[idx],
            se1=distributed.get("SE1", [0]*n)[idx],
            se2=distributed.get("SE2", [0]*n)[idx],
            mid1=distributed.get("MID1", [0]*n)[idx],
            mid2=distributed.get("MID2", [0]*n)[idx],
            record=distributed.get("Record", [0]*n)[idx],
            evaluation=distributed.get("Evaluation", [0]*n)[idx]
        )

# ==========================================================
# Validation Functions
# ==========================================================

def validate_theory(weightages):
    le_total = sum(float(w.get("LE", 0)) for w in weightages)
    se1_total = sum(float(w.get("SE1", 0)) for w in weightages)
    se2_total = sum(float(w.get("SE2", 0)) for w in weightages)

    return (
        abs(le_total - 25.0) < 0.01 and
        abs(se1_total - 30.0) < 0.01 and
        abs(se2_total - 45.0) < 0.01
    )
    
def validate_theory_practical(weightages):

    le_total = sum(float(w.get("LE", 0)) for w in weightages)
    se1_total = sum(float(w.get("SE1", 0)) for w in weightages)
    se2_total = sum(float(w.get("SE2", 0)) for w in weightages)
    mid1_total = sum(float(w.get("MID1", 0)) for w in weightages)
    mid2_total = sum(float(w.get("MID2", 0)) for w in weightages)
    record_total = sum(float(w.get("Record", 0)) for w in weightages)

    return (
        abs(le_total - 25.0) < 0.01 and
        abs(se1_total - 30.0) < 0.01 and
        abs(se2_total - 45.0) < 0.01 and
        abs(mid1_total - 20.0) < 0.01 and
        abs(mid2_total - 20.0) < 0.01 and
        abs(record_total - 60.0) < 0.01
    )

import inspect

def validate_evaluation(weightages):

    print("\n========== validate_evaluation ==========")
    print(inspect.getsource(validate_evaluation))
    print("weightages =", weightages)

    evaluation_total = sum(
        float(w.get("Evaluation", 0))
        for w in weightages
    )

    print("Evaluation Total =", evaluation_total)

    return abs(evaluation_total - 100.0) < 0.01

def validate_weightages(course_type, weightages):
    

    if course_type == "Theory":
        return validate_theory(weightages)

    elif course_type == "Theory + Practical":
        return validate_theory_practical(weightages)

    elif course_type in ("Capstone", "Capstone Project", "Internship", "Project"):
        return validate_evaluation(weightages)

    return False
# ==========================================================
# Helpers & Mode Management
# ==========================================================

def course_weightages_exist(course_id):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT COUNT(*) FROM COWeightage WHERE course_id = ?
        """, (course_id,)).fetchone()
        return row[0] > 0

def initialize_weightages(course_id):
    if not course_weightages_exist(course_id):
        generate_default_equal_weightages(course_id)

def get_weightage_mode(course_id):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT weightage_mode FROM COWeightage WHERE course_id = ? LIMIT 1
        """, (course_id,)).fetchone()
        return row["weightage_mode"] if row else "DEFAULT"

def set_weightage_mode(course_id, mode):
    with get_connection() as conn:
        conn.execute("""
            UPDATE COWeightage
            SET weightage_mode = ?, updated_at = CURRENT_TIMESTAMP
            WHERE course_id = ?
        """, (mode, course_id))
        conn.commit()

def get_assessment_pattern(course_type):
    if course_type == "Theory":
        return {"LE": 25, "SE1": 30, "SE2": 45}
    elif course_type == "Theory + Practical":
        return {"LE": 25, "SE1": 30, "SE2": 45, "MID1": 20, "MID2": 20, "Record": 60}
    elif course_type in ("Capstone", "Capstone Project", "Internship"):
        return {"Evaluation": 100}
    return {}

# ==========================================================
# Assessment Structure
# ==========================================================

def get_assessment_components(course_type):
    """
    Returns assessment components and maximum marks
    based on course type.
    """

    if course_type == "Theory":

        return {
            "LE": 25,
            "SE1": 30,
            "SE2": 45
        }

    elif course_type == "Practical":

        return {
            "MID1": 20,
            "MID2": 20,
            "Record": 60
        }

    elif course_type == "Theory + Practical":

        return {
            "LE": 25,
            "SE1": 30,
            "SE2": 45,
            "MID1": 20,
            "MID2": 20,
            "Record": 60
        }

    elif course_type in ["Capstone", "Internship"]:

        return {
            "Evaluation": 100
        }

    return {}

# ==========================================================
# Get Course Details
# ==========================================================

def get_course_details(course_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            course_code,
            course_name,
            course_type
        FROM Course
        WHERE id = ?
          AND is_active = 1
    """, (course_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)

# ==========================================================
# Get Course Assessment Details
# ==========================================================

def get_course_assessment(course_id):

    # Get course information
    course = get_course_details(course_id)

    if course is None:
        return None

    # Assessment structure
    components = get_assessment_components(
        course["course_type"]
    )

    # Course Outcomes
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            co_code
        FROM CourseOutcome
        WHERE course_id = ?
          AND is_active = 1
        ORDER BY id
    """, (course_id,))

    rows = cursor.fetchall()

    conn.close()

    cos = [
    dict(row)
    for row in rows
    ]

    return {

        "course_id": course["id"],

        "course_code": course["course_code"],

        "course_name": course["course_name"],

        "course_type": course["course_type"],

        "components": components,

        "course_outcomes": cos

    }
