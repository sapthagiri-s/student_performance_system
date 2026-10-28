# It must support:
    # 1. Add a student
    # 2. View one student
    # 3. View all students
    # 4. Search by student ID
    # 5. Update student details
    # 6. Delete a student #

import json # it includes json contents
import os 
from validation import validate_student_id, get_valid_mark, validate_age

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Fetching the folder
FILE_PATH = os.path.join(BASE_DIR, "data", "students.json") # From the student_performance_system folder, searching for data folder then file


def load_students():
    # Check whether the file exists and contains data
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        return {}

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError as error:
        print(f"Error: students.json contains invalid JSON: {error}")
        raise


def save_students(students):
    # Save the updated list back to the file
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4, ensure_ascii=False)

def check_student_id(students, student_id):
    return student_id in students

def add_student():  # Used to store the details of a student

    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot add student because the data file is corrupted.")
        return

    # Collecting the student details.
    student_id = validate_student_id()
    
    if not student_id:
        return
    
    name = input("Enter the student name : ").strip()
    if not name:
        print("Student name cannot be empty.")
        return
    
    age = validate_age()
    if not age:
        return
    
    department = input("Enter the student department : ").strip()
    if not department:
        print("Department cannot be empty.")
        return

    if not check_student_id(students, student_id):

        # Outer key = student ID, value = inner dictionary of fields
        students[student_id] = {
            "name": name,
            "age": age,
            "department": department
        }
        save_students(students)
        print(f"Student {student_id} added successfully")
    else:
        print(f"Student {student_id} already exists")

def search_student():
    student_id = validate_student_id()
    
    if not student_id:
        return
    
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot search because the data file is corrupted.")
        return

    if check_student_id(students, student_id):
        print("\nStudent found!")
        print("Id         : ",student_id)
        print("Name       : ",students[student_id].get("name"))
        print("Age        : ",students[student_id].get("age"))
        print("Department : ",students[student_id].get("department"))

    else:
        print(f"No student found with ID {student_id}")

def view_all_students():
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot display students because the data file is corrupted.")
        return

    if not students:
        print("No student records found. Please add a student first.")
        return

    for student_id, details in students.items():
        print("Id         :", student_id)
        print("Name       :", details.get("name"))
        print("Age        :", details.get("age"))
        print("Department :", details.get("department"))
        print("-" * 30)

def update_student():
    student_id = input("Enter student ID: ").strip()

    if not student_id or not all("0" <= char <= "9" for char in student_id):
        print("Student ID must contain only digits.")
        return
    
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot update because the data file is corrupted.")
        return

    if check_student_id(students, student_id):
        print("\nStudent found!\n1. Update Name\n2. Update Age\n3. Update Department\n4. Update All Details\n5. Back to Main Menu\n")

        try:
            choice = int(input("Enter the choice : "))
        except ValueError:
            print("Choice must be a number")
            return

        if(choice == 1):
            name = input("Enter the new name : ").strip()
            if not name:
                print("Student name cannot be empty.")
                return
            students[student_id].update({"name":name})
            save_students(students)
            print(f"Student {student_id} updated successfully!")
        elif(choice == 2):
            try:
                age = int(input("Enter the student age : "))
                if age < 18:
                    print("Student age must be more than 17.")
                    return
            except ValueError:
                print("Student Age must be a number")
                return
            students[student_id].update({"age":age})
            save_students(students)
            print(f"Student {student_id} updated successfully!")
        elif(choice == 3):
            department = input("Enter the new department : ").strip()
            if not department:
                print("Department cannot be empty.")
                return
            students[student_id].update({"department":department})
            save_students(students)
            print(f"Student {student_id} updated successfully!")
        elif(choice == 4):
            name = input("Enter the new name : ").strip()
            if not name:
                print("Student name cannot be empty.")
                return
            try:
                age = int(input("Enter the student age : "))
                if age < 18:
                    print("Student age must be more than 17.")
                    return
            except ValueError:
                print("Student Age must be a number")
                return
            department = input("Enter the new department : ").strip()
            if not department:
                print("Department cannot be empty.")
                return

            students[student_id].update({
                "name": name,
                "age": age,
                "department": department
            })

            save_students(students)
            print(f"Student {student_id} updated successfully!")
        elif(choice == 5):
            print("Exiting from the update student function.")
            return
        else:
            print("Invalid choice!")
            return



    else:
        print(f"No student found with ID {student_id}")

def delete_student():
    student_id = input("Enter student ID: ").strip()

    if not student_id or not all("0" <= char <= "9" for char in student_id):
        print("Student ID must contain only digits.")
        return
    
    try:
        students = load_students()
    except json.JSONDecodeError:
        print("Cannot delete because the data file is corrupted.")
        return

    if check_student_id(students, student_id):
        choice = input(
                f"Are you sure you want to delete student {student_id} "
                f"{students[student_id].get('name')}? "
                "This cannot be undone. (yes/no): "
            ).strip().lower()
        if choice in ["yes", "y"]:
            del students[student_id]
            save_students(students)
            print(f"Student {student_id} deleted successfully")
        elif choice in ["no", "n"]:
            print("Deletion cancelled. No changes made.")
        else:
            print("Invalid choice. Please type yes or no.")

