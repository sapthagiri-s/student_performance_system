import json
from student import load_students, save_students
from validation import validate_student_id, get_valid_mark

def check_subject(students, subject, student_id):
     return subject in students[student_id].get("marks", {})

def common_validation(msg, require_subject, allow_empty_marks=False):
    student_id = validate_student_id()

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
    
    marks = students[student_id].setdefault("marks", {})

    if not isinstance(marks, dict):
        print("Invalid marks data for this student.")
        return None
    if not marks and not allow_empty_marks:
        print(f"No marks found for student ID {student_id}.")
        return None

    if require_subject:
        subject = input("Enter the subject: ").strip().lower()
        if not subject:
            print("Subject cannot be empty.")
            return None
        
        return students, student_id, subject

    return students, student_id

def add_marks(): # add a subject and its marks.
    
    result = common_validation(
            "Cannot add marks because the data file is corrupted.",
            True,
            allow_empty_marks=True
        )
    if result is None:
        return
    students, student_id, subject = result
    marks = students[student_id]["marks"]
    if subject in marks:
        current = marks[subject]
        choice = input(f"{subject} already has a mark of {current}. Do you want to change it? (yes/no): ").strip().lower()
        if choice in ["no", "n"]:
            print("No changes made.")
            return
        if choice not in ["yes", "y"]:
            print("Invalid choice. Please type yes or no.")
            return

    mark = get_valid_mark(subject)
    if mark is None:
        return

    old = marks.get(subject)
    marks[subject] = mark
    save_students(students)

    if old is None:
        print(f"Mark added successfully! {students[student_id]['name']} ({student_id}) - {subject}: {mark}")
    else:
        print(f"{subject} mark updated: {old} → {mark}")

def view_marks(): # display a student's subjects and marks.
    result = common_validation("Cannot view marks because the data file is corrupted.", False)
    if result is None:
        return
    students, student_id = result
    marks = students[student_id]["marks"]
    
    print(f"\nStudent Name: {students[student_id].get('name')}\n" f"Student ID  : {student_id}\n" "------------------------------\n" "Subject              Marks\n" 
                    "------------------------------")
    for subject, mark in marks.items():
        print(f"{subject:<20} {mark}")
        
    print("------------------------------\n")

def update_marks(): # modify an existing subject's marks.
    result = common_validation("Cannot update marks because the data file is corrupted.", False)
    if result is None:
        return
    students, student_id = result
    marks = students[student_id]["marks"]
    print("Available subjects:")
    for subject, mark in marks.items():
        print(f"{subject:<20} {mark}")
    
    subject = input("\nEnter the subject to update: ").strip().lower()
    if not subject:
        print("Subject cannot be empty.")
        return

    if check_subject(students, subject, student_id):
        current_mark = marks.get(subject)
        print(f"Current mark: {current_mark}")
        mark = get_valid_mark(subject)
        if mark is None:
            return
        students[student_id]["marks"][subject] = mark
        save_students(students)
        print(f"\n{subject} mark updated successfully: {current_mark} -> {mark}")
        
    else:
        print("Subject is not present!")
        return

def delete_marks(): # remove a subject's marks.
    result = common_validation("Cannot delete marks because the data file is corrupted.", False)
    if result is None:
        return
    students, student_id = result
    marks = students[student_id]["marks"]
        
    print("Available subjects:")
    for subject, mark in marks.items():
        print(f"{subject:<20} {mark}")
    
    subject = input("\nEnter the subject to delete: ").strip().lower()
    if not subject:
        print("Subject cannot be empty.")
        return

    if check_subject(students, subject, student_id):
        choice = input(
            f"Are you sure you want to delete subject '{subject}' "
            f"for {students[student_id].get('name')} ({student_id})? "
            "This cannot be undone. (yes/no): "
        ).strip().lower()
        if choice in ["yes", "y"]:
            del students[student_id]["marks"][subject]
            save_students(students)
            print(f"{subject} subject deleted successfully")
        elif choice in ["no", "n"]:
            print("Deletion cancelled. No changes made.")
        else:
            print("Invalid choice. Please type yes or no.")
    else:
        print("Subject is not present!")
        return

def calculate_total(): # return total marks.
    result = common_validation("Cannot calculate total because the data file is corrupted.", False)
    if result is None:
        return
    students, student_id = result
    marks = students[student_id]["marks"]
        
    print(f"\nStudent Name : {students[student_id].get('name')}\n"
                f"Student ID   : {student_id}\n"
                f"Total Marks  : {sum(marks.values())}\n" f"Subjects     : {len(marks)}")
    
def calculate_average(students, student_id, allow=False): # return average marks.
    if allow:
        result = common_validation("Cannot calculate average because the data file is corrupted.", False)
        if result is None:
            return
        students, student_id = result
    marks = students[student_id]["marks"]
    
    total_marks = sum(marks.values())
    subjects = len(marks)
    average_mark = total_marks / subjects
    if allow:
        print(f"\nStudent Name : {students[student_id].get('name')}\n"
            f"Student ID   : {student_id}\n"
            f"Total Marks  : {total_marks}\n" f"Subjects     : {subjects}\n" f"Average Marks: {average_mark:.2f}")
    return total_marks, average_mark

def calculate_percentage(students, student_id, allow=False): # return percentage.
    if allow:
        result = common_validation("Cannot calculate percentage because the data file is corrupted.", False)
        if result is None:
            return
        students, student_id = result
    marks = students[student_id]["marks"]
    
    total_marks = sum(marks.values())
    subjects = len(marks)
    percentage = (total_marks/(subjects*100))*100
    if allow:
        print(f"\nStudent Name : {students[student_id].get('name')}\n"
            f"Student ID   : {student_id}\n"
            f"Total Marks  : {total_marks}\n" f"Subjects     : {subjects}\n" f"Percentage   : {percentage:.2f}%")
    return percentage

def calculate_grade(students, student_id, allow=False): # determine the grade.
    if allow:
        result = common_validation("Cannot calculate grade because the data file is corrupted.", False)
        if result is None:
            return
        students, student_id = result
    marks = students[student_id]["marks"]
    total_marks = sum(marks.values())
    subjects = len(marks)
    percentage = (total_marks/(subjects*100))*100
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else: 
        grade = "F"
    if allow:
        print(f"\nStudent Name : {students[student_id].get('name')}\n"
            f"Student ID   : {student_id}\n" f"Percentage   : {percentage:.2f}%\n" f"Grade        : {grade}\n")
    return grade