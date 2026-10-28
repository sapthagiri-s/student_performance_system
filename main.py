
from student import (
    add_student,
    view_all_students,
    search_student,
    update_student,
    delete_student
)

from marks import (
    add_marks,
    view_marks,
    update_marks,
    delete_marks,
    calculate_total,
    calculate_average,
    calculate_percentage,
    calculate_grade
)

from attendance import (
    mark_attendance,
    view_attendance,
    update_attendance,
    calculate_attendance_percentage
)

from reports import (
    student_report,
    class_report,
    top_performer,
    department_report
)

from student import load_students


def get_choice():
    try:
        return int(input("Enter your choice: ").strip())
    except ValueError:
        print("Invalid input! Please enter a number.")
        return None


def student_menu():
    while True:
        print("\n========== STUDENT MANAGEMENT ==========")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Back to Main Menu")
        print("========================================")

        choice = get_choice()

        if choice == 1:
            add_student()
        elif choice == 2:
            view_all_students()
        elif choice == 3:
            search_student()
        elif choice == 4:
            update_student()
        elif choice == 5:
            delete_student()
        elif choice == 6:
            break
        elif choice is not None:
            print("Invalid choice! Select 1 to 6.")


def marks_menu():
    while True:
        print("\n========== MARKS MANAGEMENT ==========")
        print("1. Add Marks")
        print("2. View Marks")
        print("3. Update Marks")
        print("4. Delete Marks")
        print("5. Calculate Total")
        print("6. Calculate Average")
        print("7. Calculate Percentage")
        print("8. Calculate Grade")
        print("9. Back to Main Menu")
        print("======================================")

        choice = get_choice()

        if choice == 1:
            add_marks()
        elif choice == 2:
            view_marks()
        elif choice == 3:
            update_marks()
        elif choice == 4:
            delete_marks()
        elif choice == 5:
            calculate_total()
        elif choice == 6:
            calculate_average({}, 0,allow=True)
        elif choice == 7:
            calculate_percentage({}, 0,allow=True)
        elif choice == 8:
            calculate_grade({}, 0,allow=True)
        elif choice == 9:
            break
        elif choice is not None:
            print("Invalid choice! Select 1 to 9.")

def attendance_menu():
    while True:
        print("\n========== ATTENDANCE MANAGEMENT ==========")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Update Attendance")
        print("4. Calculate Attendance Percentage")
        print("5. Back to Main Menu")
        print("===========================================")

        choice = get_choice()

        if choice == 1:
            mark_attendance()
        elif choice == 2:
            view_attendance()
        elif choice == 3:
            update_attendance()
        elif choice == 4:
            calculate_attendance_percentage({},0,allow=True)
        elif choice == 5:
            break
        elif choice is not None:
            print("Invalid choice! Select 1 to 5.")





def reports_menu():
    while True:
        print("\n========== REPORTS ==========")
        print("1. Student Report")
        print("2. Class Report")
        print("3. Top Performer")
        print("4. Department Report")
        print("5. Back to Main Menu")
        print("=============================")

        choice = get_choice()

        if choice == 1:
            student_report()
        elif choice == 2:
            class_report()
        elif choice == 3:
            top_performer()
        elif choice == 4:
            department_report()
        elif choice == 5:
            break
        elif choice is not None:
            print("Invalid choice! Select 1 to 5.")


def main():
    while True:
        print("\n==============================================")
        print("  STUDENT PERFORMANCE MANAGEMENT SYSTEM")
        print("==============================================")
        print("1. Student Management")
        print("2. Marks Management")
        print("3. Attendance Management")
        print("4. Reports")
        print("5. Exit")
        print("==============================================")

        choice = get_choice()

        if choice == 1:
            student_menu()
        elif choice == 2:
            marks_menu()
        elif choice == 3:
            attendance_menu()
        elif choice == 4:
            reports_menu()
        elif choice == 5:
            print("\nExiting Student Performance Management System.")
            print("Thank you!")
            break
        elif choice is not None:
            print("Invalid choice! Select 1 to 5.")


if __name__ == "__main__":
    main()
