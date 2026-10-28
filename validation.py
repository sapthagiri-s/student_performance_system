def validate_student_id():
    student_id = input("Enter student ID: ").strip()
    if not student_id or not all("0" <= char <= "9" for char in student_id):
        print("Student ID must contain only digits.")
        return None
    
    return student_id

def get_valid_mark(subject):
    try:
        mark = int(input(f"Enter the {subject} mark (0-100): "))
    except ValueError:
        print("Mark must be a number.")
        return None

    if not 0 <= mark <= 100:
        print("Mark must be between 0 and 100.")
        return None
    return mark

def validate_age():
    try:
        age = int(input("Enter the student age : "))
        if age < 18:
            print("Student age must be more than 17.")
            return
    except ValueError:
        print("Student Age must be a number")
        return
    
    return age
