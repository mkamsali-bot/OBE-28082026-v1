import sqlite3
from io import BytesIO

import pandas as pd


# ==========================================================
# Database
# ==========================================================

DATABASE = "obe.db"


def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================================
# Assessment Patterns
# ==========================================================

ASSESSMENT_PATTERNS = {
    "Theory": ["LE", "SE1", "SE2"],

    "Theory + Practical": [
        "LE",
        "SE1",
        "SE2",
        "MID1",
        "MID2",
        "Record"
    ],

    "Project": ["Evaluation"],          # <-- ADD THIS
    "Capstone": ["Evaluation"],
    "Capstone Project": ["Evaluation"],
    "Internship": ["Evaluation"],
}

# ==========================================================
# Get Assessment Components
# ==========================================================

def get_assessment_components(course_type):

    return ASSESSMENT_PATTERNS.get(

        course_type,

        []

    )


# ==========================================================
# Excel Column Names
# ==========================================================

def get_excel_columns(course_type):

    components = get_assessment_components(

        course_type

    )

    return [

        "Reg No.",

        "Student Name",

        *components

    ]


# ==========================================================
# Read Marks Excel
# ==========================================================

def read_marks_excel(

    file_bytes,

    course_type

):

    try:

        df = pd.read_excel(

            BytesIO(file_bytes)

        )

    except Exception as exc:

        return {

            "success": False,

            "error": f"Unable to read Excel file: {exc}",

            "data": None

        }

    # ------------------------------------------------------
    # Clean column names
    # ------------------------------------------------------

    df.columns = [

        str(column).strip()

        for column in df.columns

    ]

    # ------------------------------------------------------
    # Expected columns
    # ------------------------------------------------------

    expected_columns = get_excel_columns(

        course_type

    )

    # ------------------------------------------------------
    # Check missing columns
    # ------------------------------------------------------

    missing_columns = [

        column

        for column in expected_columns

        if column not in df.columns

    ]

    if missing_columns:

        return {

            "success": False,

            "error": (

                "Missing required columns: "

                + ", ".join(missing_columns)

            ),

            "data": None

        }

    # ------------------------------------------------------
    # Remove completely empty rows
    # ------------------------------------------------------

    df = df.dropna(

        how="all"

    ).copy()

    return {

        "success": True,

        "error": None,

        "data": df

    }
    # ==========================================================
# Maximum Marks
# ==========================================================

MAX_MARKS = {

    "LE": 25,

    "SE1": 30,

    "SE2": 45,

    "MID1": 20,

    "MID2": 20,

    "Record": 60,

    "Evaluation": 100

}


# ==========================================================
# Validate One Marks Value
# ==========================================================

def validate_mark(value, component):

    # Empty value
    if pd.isna(value):

        return False, "Mark is missing"

    # Convert to number
    try:

        mark = float(value)

    except (ValueError, TypeError):

        return False, "Mark must be numeric"

    # Maximum mark
    maximum = MAX_MARKS.get(component)

    if maximum is None:

        return False, f"Unknown assessment component: {component}"

    # Range validation
    if mark < 0:

        return False, "Mark cannot be negative"

    if mark > maximum:

        return False, (
            f"Mark cannot exceed {maximum} for {component}"
        )

    return True, None


# ==========================================================
# Validate Marks Excel Data
# ==========================================================

def validate_marks_data(

    df,

    course_type

):

    errors = []

    valid_rows = []

    components = get_assessment_components(

        course_type

    )

    # ------------------------------------------------------
    # Check course type
    # ------------------------------------------------------

    if not components:

        return {

            "valid": False,

            "errors": [

                f"Unsupported course type: {course_type}"

            ],

            "valid_rows": [],

            "total_rows": len(df)

        }

    # ------------------------------------------------------
    # Check duplicate Reg No.
    # ------------------------------------------------------

    duplicate_reg_nos = (

        df["Reg No."]

        .astype(str)

        .str.strip()

        .duplicated(keep=False)

    )

    # ------------------------------------------------------
    # Validate each row
    # ------------------------------------------------------

    for index, row in df.iterrows():

        excel_row = index + 2

        row_errors = []

        # --------------------------------------------------
        # Reg No.
        # --------------------------------------------------

        reg_no = str(

            row["Reg No."]

        ).strip()

        if not reg_no or reg_no.lower() == "nan":

            row_errors.append(

                "Reg No. is missing"

            )

        elif duplicate_reg_nos.loc[index]:

            row_errors.append(

                f"Duplicate Reg No.: {reg_no}"

            )

        # --------------------------------------------------
        # Student Name
        # --------------------------------------------------

        student_name = str(

            row["Student Name"]

        ).strip()

        if (

            not student_name

            or student_name.lower() == "nan"

        ):

            row_errors.append(

                "Student Name is missing"

            )

        # --------------------------------------------------
        # Assessment Marks
        # --------------------------------------------------

        row_marks = {}

        for component in components:

            valid, error = validate_mark(

                row[component],

                component

            )

            if not valid:

                row_errors.append(

                    f"{component}: {error}"

                )

            else:

                row_marks[component] = float(

                    row[component]

                )

        # --------------------------------------------------
        # Store error
        # --------------------------------------------------

        if row_errors:

            errors.append({

                "row": excel_row,

                "reg_no": reg_no,

                "errors": row_errors

            })

        else:

            valid_rows.append({

                "reg_no": reg_no,

                "student_name": student_name,

                "marks": row_marks

            })

    # ------------------------------------------------------
    # Result
    # ------------------------------------------------------

    return {

        "valid": len(errors) == 0,

        "errors": errors,

        "valid_rows": valid_rows,

        "total_rows": len(df),

        "valid_count": len(valid_rows),

        "error_count": len(errors)

    }
    # ==========================================================
# Generate Marks Excel Template
# ==========================================================

def generate_marks_template(course_type):

    components = get_assessment_components(
        course_type
    )

    if not components:

        raise ValueError(
            f"Unsupported course type: {course_type}"
        )

    # ------------------------------------------------------
    # Excel columns
    # ------------------------------------------------------

    columns = [

        "Reg No.",

        "Student Name",

        *components

    ]

    # ------------------------------------------------------
    # Create empty DataFrame
    # ------------------------------------------------------

    df = pd.DataFrame(

        columns=columns

    )

    # ------------------------------------------------------
    # Create Excel file in memory
    # ------------------------------------------------------

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Marks"

        )

        worksheet = writer.sheets["Marks"]

        # --------------------------------------------------
        # Set column widths
        # --------------------------------------------------

        worksheet.column_dimensions["A"].width = 18

        worksheet.column_dimensions["B"].width = 30

        for column_number in range(

            3,

            len(columns) + 1

        ):

            column_letter = (

                worksheet.cell(

                    row=1,

                    column=column_number

                ).column_letter

            )

            worksheet.column_dimensions[
                column_letter
            ].width = 15

    output.seek(0)

    return output.getvalue()
    # ==========================================================
# Prepare Marks for Database
# ==========================================================

def prepare_marks_for_import(

    validation_result,

    course_id,

    course_type

):

    if not validation_result.get("valid_rows"):

        return []

    components = get_assessment_components(

        course_type

    )

    import_rows = []

    for row in validation_result["valid_rows"]:

        reg_no = row["reg_no"]

        student_name = row["student_name"]

        marks = row["marks"]

        for component in components:

            import_rows.append({

                "course_id": course_id,

                "reg_no": reg_no,

                "student_name": student_name,

                "assessment_component": component,

                "marks": marks[component]

            })

    return import_rows
    # ==========================================================
# Import Marks into Database
# ==========================================================

def import_marks(
    import_rows,
    course_id,
    course_type=None,
    replace_existing=True
):
    """
    Import validated marks into the marks table.

    Parameters
    ----------
    import_rows : list
        Output of prepare_marks_for_import()

    course_id : int

    course_type : str
        Theory
        Theory + Practical
        Capstone
        Internship

    replace_existing : bool
    """

    if not import_rows:
        return {
            "success": False,
            "message": "No marks available for import.",
            "imported": 0
        }

    conn = get_connection()
    cursor = conn.cursor()

    imported = 0

    try:

        # --------------------------------------------
        # Replace existing marks (optional)
        # --------------------------------------------

        if replace_existing:

            cursor.execute(
                """
                DELETE FROM marks
                WHERE course_id = ?
                """,
                (course_id,)
            )

        # --------------------------------------------
        # Insert every assessment component
        # --------------------------------------------

        for row in import_rows:

            cursor.execute(
                """
                INSERT INTO marks
                (
                    course_id,
                    reg_no,
                    student_name,
                    assessment_component,
                    marks,
                    created_at,
                    updated_at
                )
                VALUES
                (
                    ?, ?, ?, ?, ?,
                    CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP
                )
                """,
                (
                    course_id,
                    row["reg_no"],
                    row["student_name"],
                    row["assessment_component"],
                    row["marks"]
                )
            )

            imported += 1

        conn.commit()

        return {
            "success": True,
            "message": f"{imported} marks imported successfully.",
            "imported": imported
        }

    except Exception as exc:

        conn.rollback()

        return {
            "success": False,
            "message": str(exc),
            "imported": 0
        }

    finally:

        conn.close()