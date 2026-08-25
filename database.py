import sqlite3
from pathlib import Path

DB_NAME = "obe.db"


import os
import sqlite3

DB_NAME = "obe.db"

def get_connection():

    print("Current Working Directory:", os.getcwd())
    print("Database File:", os.path.abspath(DB_NAME))

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")

    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. DEPARTMENT MASTER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Department (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_code TEXT NOT NULL UNIQUE,
            department_name TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)

    # 2. PROGRAM MASTER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Program (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_code TEXT NOT NULL UNIQUE,
            program_name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            duration INTEGER DEFAULT 4,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE
        )
    """)

    # 3. FACULTY MASTER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_code TEXT NOT NULL UNIQUE,
            faculty_name TEXT NOT NULL,
            designation TEXT,
            email TEXT,
            mobile TEXT,
            department_id INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE SET NULL
        )
    """)

    # 4. COURSE MASTER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            department_id INTEGER NOT NULL,
            program_id INTEGER NOT NULL,
            faculty_id INTEGER,
            semester INTEGER NOT NULL,
            credits REAL DEFAULT 0,
            regulation TEXT,
            course_type TEXT NOT NULL DEFAULT 'Theory',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE,
            FOREIGN KEY (program_id) REFERENCES Program(id) ON DELETE CASCADE,
            FOREIGN KEY (faculty_id) REFERENCES Faculty(id) ON DELETE SET NULL
        )
    """)

    # 5. PROGRAM OUTCOME (PO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProgramOutcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER NOT NULL,
            po_code TEXT NOT NULL,
            po_description TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE,
            UNIQUE(department_id, po_code)
        )
    """)

    # 6. PROGRAM SPECIFIC OUTCOME (PSO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProgramSpecificOutcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER NOT NULL,
            pso_code TEXT NOT NULL,
            pso_description TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES Department(id) ON DELETE CASCADE,
            UNIQUE(department_id, pso_code)
        )
    """)

    # 7. COURSE OUTCOME (CO)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseOutcome (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            co_code TEXT NOT NULL,
            co_description TEXT NOT NULL,
            blooms_level TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
            UNIQUE(course_id, co_code)
        )
    """)

    # 8. CO - PO / PSO MAPPING
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CO_PO_Mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            co_id INTEGER NOT NULL,
            po1 INTEGER DEFAULT 0, po2 INTEGER DEFAULT 0, po3 INTEGER DEFAULT 0,
            po4 INTEGER DEFAULT 0, po5 INTEGER DEFAULT 0, po6 INTEGER DEFAULT 0,
            po7 INTEGER DEFAULT 0, po8 INTEGER DEFAULT 0, po9 INTEGER DEFAULT 0,
            po10 INTEGER DEFAULT 0, po11 INTEGER DEFAULT 0, po12 INTEGER DEFAULT 0,
            pso1 INTEGER DEFAULT 0, pso2 INTEGER DEFAULT 0, pso3 INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
            FOREIGN KEY (co_id) REFERENCES CourseOutcome(id) ON DELETE CASCADE,
            UNIQUE(course_id, co_id)
        )
    """)

    # 9. CO WEIGHTAGE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COWeightage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            co_id INTEGER NOT NULL,
            weightage_mode TEXT NOT NULL DEFAULT 'DEFAULT',
            le_weightage REAL DEFAULT 0,
            se1_weightage REAL DEFAULT 0,
            se2_weightage REAL DEFAULT 0,
            mid1_weightage REAL DEFAULT 0,
            mid2_weightage REAL DEFAULT 0,
            record_weightage REAL DEFAULT 0,
            evaluation_weightage REAL DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE,
            FOREIGN KEY (co_id) REFERENCES CourseOutcome(id) ON DELETE CASCADE,
            UNIQUE(course_id, co_id)
        )
    """)

    # 10. STUDENT MASTER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL UNIQUE,
            student_name TEXT NOT NULL,
            gender TEXT,
            batch TEXT,
            semester INTEGER,
            section TEXT,
            email TEXT,
            mobile TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    """)

    # 11. MARKS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            reg_no TEXT NOT NULL,
            student_name TEXT NOT NULL,
            assessment_component TEXT NOT NULL,
            marks REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES Course(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS IndirectAttainment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        co_id INTEGER NOT NULL,
        indirect_percentage REAL NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(course_id) REFERENCES Course(id),
        FOREIGN KEY(co_id) REFERENCES CourseOutcome(id)
        )
    """)

    # Safe Schema Migrations for Course Table
    migrations = [
        "ALTER TABLE Course ADD COLUMN course_type TEXT DEFAULT 'Theory'",
        "ALTER TABLE Course ADD COLUMN regulation TEXT",
        "ALTER TABLE Course ADD COLUMN credits REAL DEFAULT 0"
    ]
    for migration in migrations:
        try:
            cursor.execute(migration)
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Safe Schema Migrations for Marks Table
    cursor.execute("PRAGMA table_info(Marks)")
    marks_columns = [row[1] for row in cursor.fetchall()]

    additional_marks_columns = [
        ("reg_no", "TEXT"),
        ("student_name", "TEXT"),
        ("assessment_component", "TEXT"),
        ("marks", "REAL"),
        ("created_at", "TIMESTAMP"),
        ("updated_at", "TIMESTAMP")
    ]

    for col_name, col_type in additional_marks_columns:
        if col_name not in marks_columns:
            cursor.execute(f"ALTER TABLE Marks ADD COLUMN {col_name} {col_type}")

    # Performance Index Optimizations
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_marks_course_reg ON Marks(course_id, reg_no);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_co_course ON CourseOutcome(course_id);")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("=" * 60)
    print("OBE Analytics Pro Database Created Successfully")
    print(f"Database File : {Path(DB_NAME).resolve()}")
    print("=" * 60)