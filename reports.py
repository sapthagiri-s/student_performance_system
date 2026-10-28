import json
from student import load_students
from marks import calculate_grade, calculate_percentage, calculate_average
from attendance import calculate_attendance_percentage
from validation import validate_student_id
def common_validation(msg):
    
    student_id = validate_student_id()
    if not student_id:
        return
    try:
        students = load_students()
    except json.JSONDecodeError:
        print(msg)
        return None

    if student_id not in students:
        print(f"No student found with ID {student_id}")
        return None
    if not isinstance(students[student_id], dict):
        print("Invalid student record.")
        return None
    
    return students, student_id

def student_report(): # display student details, subject marks, total, average, percentage, grade, and attendance percentage.

    result = common_validation("Cannot get student report because the data file is corrupted.")
    if result is None:
            return
            
    students, student_id = result
    attendance = students[student_id].get("attendance", {})
    if not isinstance(attendance, dict):
        print("Invalid attendance data for this student.")
        return None
    if not attendance:
        print(f"No attendance found for student ID {student_id}.")
        return 0, 0, 0.0
    
    print("========== STUDENT PERFORMANCE REPORT ==========\n\n" f"Student ID   : {student_id}\n" f"Name         : {students[student_id].get('name')}\n" 
          f"Age          : {students[student_id].get('age')}\n" f"Department   : {students[student_id].get('department')}\n")
    marks = students[student_id].get("marks", {})
    if not isinstance(marks, dict):
            print("Invalid marks data for this student.")
            return None
    if not marks:
        print(f"No marks found for student ID {student_id}.")
        return None
    
    print("--------------- ACADEMIC PERFORMANCE -----------\n" f"Subject              Marks")
    for subject, mark in marks.items():
            print(f"{subject:<20} {mark}")
            
    mark_result = calculate_average(students, student_id, allow=False)
    if mark_result is None:
        return
    total_mark, average = mark_result
    
    percentage = calculate_percentage(students, student_id, allow=False)
    if percentage is None:
        return
    
    grade = calculate_grade(students, student_id, allow=False)
    if grade is None:
        return
    
    print(f"\nTotal Marks  : {total_mark}\n" f"Average      : {average:.2f}\n" f"Percentage   : {percentage:.2f}%\n" f"Grade        : {grade}\n")

    attendance_result = calculate_attendance_percentage(students, student_id, allow=False)
    total_day, present_count, attendance_percentage = attendance_result
    absent_count = total_day - present_count
    print("--------------- ATTENDANCE ---------------------\n" f"Total Days   : {total_day}\n" f"Present      : {present_count}\n" f"Absent       : {absent_count}\n" f"Percentage   : {attendance_percentage:.2f}%\n\n" "================================================\n")


def class_report(): # display a summary of all students and their overall performance.
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot get class report because the data file is corrupted.")
        return None
    if not students:
        print("No student records found.")
        return
    
    print("========== CLASS PERFORMANCE REPORT ==========\n" "ID     Name        Department   Total   Average   Grade   Attendance\n" "--------------------------------------------------------------------")
    
    for student_id in students:
        mark_result = calculate_average(students, student_id, allow=False)
        if mark_result is None:
            return
        total_mark, average = mark_result
        
        grade = calculate_grade(students, student_id, allow=False)
        if grade is None:
            return
        attendance_result = calculate_attendance_percentage(students, student_id, allow=False)
        total_day, present_count, attendance_percentage = attendance_result
        
        print(f"{student_id}    " f"{students[student_id].get('name')}       "f"{students[student_id].get('department')} "f"          {total_mark}     "f"{average:.2f}     "f"{grade}       "f"{attendance_percentage:.2f}%")
        
    print("===============================================\n")


def top_performer(): # identify the student with the highest average marks.
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot get top performer report because the data file is corrupted.")
        return None
    if not students:
        print("No student records found.")
        return
    top_performers = {}
    
    for student_id in students:
        mark_result = calculate_average(students, student_id, allow=False)
        if mark_result is None:
            return
        total_mark, average = mark_result
        
        top_performers.update({student_id : average})
    
    if not top_performers:
        print("No valid marks found.")
        return

    highest = max(top_performers.values())
    best_students = []
    for st_id, avg in top_performers.items():
        if avg == highest:
            best_students.append(st_id)
    
    print("========== TOP PERFORMER ==========\n")
    for student_id in best_students:
        mark_result = calculate_average(students, student_id, allow=False)
        if mark_result is None:
            return
        total_mark, average = mark_result
        if average is not None:
            grade = calculate_grade(students, student_id, allow=False)
            if grade is None:
                return
            
            print(f"Student ID   : {student_id}\n" f"Name         : {students[student_id].get('name')}\n"
                    f"Department   : {students[student_id].get('department')}\n"f"Total Marks  : {total_mark}\n"
                    f"Average      : {average:.2f}\n"f"Grade        : {grade}\n")
        
    print("===================================")
    
def department_report():
    department = input("Enter the department : ").strip()
    if not department:
        print("Department cannot be empty.")
        return
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot get department report because the data file is corrupted.")
        return None
    if not students:
        print("No student records found.")
        return
    print("========== DEPARTMENT PERFORMANCE REPORT ==========\n" f"Department: {department}\n" "ID     Name       Total   Average   Grade   Attendance\n" "------------------------------------------------------\n")

    for student_id, student in students.items():
        if student.get("department", "").lower() == department.lower():
            mark_result = calculate_average(students, student_id, allow=False)
            if mark_result is None:
                return
            total_mark, average = mark_result
            
            grade = calculate_grade(students, student_id, allow=False)
            if grade is None:
                return
            attendance_result = calculate_attendance_percentage(students, student_id, allow=False)
            total_day, present_count, attendance_percentage = attendance_result
            
            print(f"{student_id}    " f"{students[student_id].get('name')}     "f" {total_mark}     "f"{average:.2f}     "f"{grade}       "f"{attendance_percentage:.2f}%")
                    
    print("====================================================")
    
