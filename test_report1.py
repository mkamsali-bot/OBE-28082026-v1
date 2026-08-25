from services.nba_report1_service import get_student_marks

students = get_student_marks(1)

print("Students =", len(students))

print()

for s in students[:5]:
    print(s)