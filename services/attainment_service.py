from services.co_po_service import get_course_mappings
from services.co_service import get_co_by_id
from services.co_weightage_service import get_weightages
from services.marks_service import get_marks_by_course
from services.indirect_attainment_service import get_indirect_attainment



def get_course_marks(course_id):
    """Returns all uploaded marks for the selected course."""
    return get_marks_by_course(course_id)


def build_student_dictionary(marks):
    """Organize marks course-wise into a student dictionary."""

    students = {}

    for row in marks:

        reg_no = row["reg_no"]

        if reg_no not in students:

            students[reg_no] = {
                "reg_no": row["reg_no"],
                "student_name": row["student_name"],
                "marks": {},
            }

        students[reg_no]["marks"][row["assessment_component"]] = row["marks"]

    return students


def get_student(reg_no, students):
    """Returns a student dictionary if present.

    Otherwise returns None.
    """

    return students.get(reg_no)


def get_student_marks(reg_no, students):
    """Returns the marks dictionary of a student."""

    student = students.get(reg_no)

    if student is None:
        return {}

    return student["marks"]


def apply_co_weightages(student_marks, co_weightages):
    """Apply CO weightages to one student's marks."""

    print("\n==============================")
    print("Student Marks:", student_marks)

    co_scores = {}

    for row in co_weightages:

        print("\nCO:", row["co_id"])
        print("Weightages:", row["values"])

        score = 0.0

        # Maximum marks for each assessment component
        max_marks = {
            "LE": 25,
            "SE1": 30,
            "SE2": 45,
            "MID1": 20,
            "MID2": 20,
            "Record": 60,
            "Evaluation": 100,
        }

        for component, weight in row["values"].items():
            marks = float(student_marks.get(component, 0))
            maximum = max_marks.get(component, 100)

            score += (marks / maximum) * weight

        print("Calculated Score =", score)

        co_scores[row["co_id"]] = round(score, 2)

    return co_scores


def calculate_course_attainment(course_id):
    """Calculate CO scores for every student in a course.

    Returns:
    {
        reg_no: {
            "student_name": "...",
            "co_scores": {
                co_id: score
            }
        }
    }
    """

    # Read all uploaded marks
    marks = get_course_marks(course_id)
    print("Sample Marks Row:")
    print(marks[0] if marks else "No Marks Found")

    # Organize student-wise
    students = build_student_dictionary(marks)

    # Read CO weightages
    weightages = get_weightages(course_id)
    print("\n===== CO WEIGHTAGES =====")
    for w in weightages:
        print(w)

    results = {}

    # Process each student
    for reg_no, student in students.items():

        student_marks = get_student_marks(reg_no, students)

        co_scores = apply_co_weightages(student_marks, weightages)

        results[reg_no] = {
            "student_name": student["student_name"],
            "co_scores": co_scores,
        }
    print("\n===== COURSE ATTAINMENT =====")
    for reg_no, data in results.items():
        print(f"Student: {reg_no}")
        print("CO Scores:", data["co_scores"])
    return results


def calculate_co_attainment_percentage(course_id, target_score):
    """Calculate CO attainment percentage for a course.

    Returns:
    {
        co_id: {
            "achieved": int,
            "total": int,
            "percentage": float
        }
    }
    """

    student_results = calculate_course_attainment(course_id)
    print("\n===== STUDENT RESULTS =====")
    for reg_no, student in student_results.items():
        print(reg_no, student)

    summary = {}

    total_students = len(student_results)

    for student in student_results.values():

        for co_id, score in student["co_scores"].items():

            if co_id not in summary:

                summary[co_id] = {"achieved": 0, "total": total_students}

            print(
                f"CO={co_id}, Score={score}, Target={target_score}, "
                f"Achieved={score >= target_score}"
            )

            if score >= target_score:
                summary[co_id]["achieved"] += 1

    for co_id in summary:

        achieved = summary[co_id]["achieved"]
        total = summary[co_id]["total"]

        summary[co_id]["percentage"] = round((achieved / total) * 100, 2)

        # Add the actual CO code (CO1, CO2, ...)
        co = get_co_by_id(co_id)

        if co:
            summary[co_id]["co_code"] = co["co_code"]
        else:
            summary[co_id]["co_code"] = f"CO{co_id}"

    return summary


def get_course_co_summary(course_id, target_score):
    """Returns a course-wise CO attainment summary."""

    attainment = calculate_co_attainment_percentage(course_id, target_score)

    summary = []

    for co_id, data in attainment.items():

        co = get_co_by_id(co_id)

        summary.append(
            {
                "co_id": co_id,
                "co_code": co["co_code"] if co else f"CO{co_id}",
                "students_achieved": data["achieved"],
                "total_students": data["total"],
                "attainment_percentage": data["percentage"],
            }
        )

    return summary


def calculate_po_attainment(course_id, target_score):
    """Calculate PO attainment for a course."""
    from services.final_attainment_service import calculate_final_co_attainment

    final_co = calculate_final_co_attainment(
        course_id,
        target_score
    )
    mappings = get_course_mappings(course_id)

    po_scores = {}

    # Convert CO summary list into dictionary
    co_attainment = {}

    for co_id, values in final_co.items():
        co_attainment[co_id] = values["final"]

    

    # Calculate PO scores
    for mapping in mappings:
        

        co_id = mapping["co_id"]
        

        if co_id not in co_attainment:
            continue

        

        co_percentage = co_attainment[co_id]

        for i in range(1, 13):

            po_name = f"po{i}"

            strength = mapping[po_name]

            if strength == 0:
                continue

            if po_name not in po_scores:

                po_scores[po_name] = {"weighted_sum": 0, "strength_sum": 0}

            po_scores[po_name]["weighted_sum"] += co_percentage * strength

            po_scores[po_name]["strength_sum"] += strength

    # Final weighted average
    result = {}

    for po, data in po_scores.items():

        result[po.upper()] = round(
            data["weighted_sum"] / data["strength_sum"], 2
        )

    return result


def calculate_pso_attainment(course_id, target_score):
    from services.final_attainment_service import calculate_final_co_attainment

    final_co = calculate_final_co_attainment(
        course_id,
        target_score
    )
    mappings = get_course_mappings(course_id)

    pso_scores = {}

    co_attainment = {}

    for co_id, values in final_co.items():
        co_attainment[co_id] = values["final"]

    for mapping in mappings:

        co_id = mapping["co_id"]

        if co_id not in co_attainment:
            continue

        percentage = co_attainment[co_id]

        for pso in ["pso1", "pso2", "pso3"]:

            strength = mapping[pso]

            if strength == 0:
                continue

            if pso not in pso_scores:
                pso_scores[pso] = {"weighted_sum": 0, "strength_sum": 0}

            pso_scores[pso]["weighted_sum"] += percentage * strength
            pso_scores[pso]["strength_sum"] += strength

    result = {}

    for pso, values in pso_scores.items():

        result[pso.upper()] = round(
            values["weighted_sum"] / values["strength_sum"], 2
        )

    return result

