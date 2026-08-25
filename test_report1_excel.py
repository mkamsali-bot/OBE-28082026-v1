from services.report1_excel_service import generate_student_marks_excel

wb = generate_student_marks_excel(2)

wb.save("report1_test.xlsx")

print("Success")