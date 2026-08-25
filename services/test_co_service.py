from services.co_weightage_service import (
    get_courses,
    get_course_details,
    get_course_cos,
    get_course_assessment_components
)

courses = get_courses()

course_id = courses[0]["course_id"]

print(get_course_details(course_id))

print("\nCOs")
print(get_course_cos(course_id))

print("\nAssessment Components")
print(get_course_assessment_components(course_id))