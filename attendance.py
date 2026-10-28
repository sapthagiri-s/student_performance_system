import json
from student import load_students, save_students
from datetime import datetime

def common_validation(msg, allow_empty_attendance=False):
    student_id = input("Enter student ID: ").strip()
    if not student_id or not all("0" <= char <= "9" for char in student_id):
        print("Student ID must contain only digits.")
        return None

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
    
    attendance = students[student_id].setdefault("attendance", {})

    if not isinstance(attendance, dict):
        print("Invalid attendance data for this student.")
        return None
    if not attendance and not allow_empty_attendance:
        print(f"No attendance found for student ID {student_id}.")
        return None

    return students, student_id

def mark_attendance(): # mark a student as present or absent for a date.
    result = common_validation(
            "Cannot mark attendance because the data file is corrupted.",
            allow_empty_attendance=True
        )
    if result is None:
        return
        
    students, student_id = result
    attendance = students[student_id]["attendance"]
    
    date = input("Enter attendance date (YYYY-MM-DD): ").strip()   
    
    try:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date. Please use YYYY-MM-DD format.")
        return
    
    status = input("Enter attendance status (Present/Absent): ").strip().lower()
    if status not in ["present", "absent"]:
        print("Status must be Present or Absent.")
        return

    status = status.capitalize()
    
    if date in attendance:
        print("Attendance already marked for this date.")
        return

    attendance[date] = status
    save_students(students)
    print("\nAttendance marked successfully!\n" f"Student ID: {student_id}\n" f"Date      : {date}\n" f"Status    : {status}\n")


def view_attendance(): # display attendance records for a student.
    result = common_validation(
        "Cannot view attendance because the data file is corrupted.",
        allow_empty_attendance=False
    )
    if result is None:
        return
        
    students, student_id = result
    attendance = students[student_id]["attendance"]
    
    print(f"\nStudent Name: {students[student_id].get('name')}\n" f"Student ID  : {student_id}\n" "--------------------------------\n" "Date            Status\n"
          "--------------------------------")
    
    for date, status in attendance.items():
        print(f"{date}      " f"{status}")

    print("--------------------------------")
    


def update_attendance(): # correct an existing attendance record.
    result = common_validation(
            "Cannot update attendance because the data file is corrupted.",
            allow_empty_attendance=False
        )
    if result is None:
        return
            
    students, student_id = result
    attendance = students[student_id]["attendance"]
    
    print("Existing attendance:")
    
    for date, status in attendance.items():
        print(f"{date}      " f"{status}")
        
    date = input("Enter attendance date (YYYY-MM-DD): ").strip()   
        
    try:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date. Please use YYYY-MM-DD format.")
        return
    if date not in attendance:
        print("No attendance record found for this date.")
        return
    current_status = attendance[date]
    print(f"Current status: {current_status}")
    status = input("Enter new status (Present/Absent): ").strip().lower()
    if status not in ["present", "absent"]:
        print("Status must be Present or Absent.")
        return

    status = status.capitalize()
    
    if status == current_status:
        print("Attendance status is already the same. No changes made.")
        return
    
    attendance[date] = status
    save_students(students)
    print("Attendance updated successfully!\n" f"{date}: " f"{current_status} -> " f"{status}")


def calculate_attendance_percentage(students, student_id, allow=False): # calculate the student's attendance percentage.
    if allow:
        result = common_validation(
                    "Cannot calculate attendance percentage because the data file is corrupted.",
                    allow_empty_attendance=False
                )
        if result is None:
            return
                
        students, student_id = result
    attendance = students[student_id]["attendance"]
    
    total_attendance = len(attendance)
    
    present_count = 0
    for status in attendance.values():
        if status == "Present":
            present_count += 1

    attendance_percentage = (present_count / total_attendance) * 100
    if allow:
        print(f"Student Name          : {students[student_id].get('name')}\n" f"Student ID            : {student_id}\n" f"Total Attendance Days : {total_attendance}\n" 
          f"Days Present          : {present_count}\n" f"Attendance Percentage: {attendance_percentage:.2f}%\n")

    return total_attendance, present_count, attendance_percentage