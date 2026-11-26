import os

COURSE_FILE = "text/courses.txt"


def display_menu():
    print("\n" + "=" * 45)
    print("DOODLE COURSE MANAGEMENT")
    print("=" * 45)
    print("1. Add Course")
    print("2. Display and Search Courses")
    print("3. Update Course")
    print("4. Delete Course")
    print("5. Back to Main Menu")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")


def ensure_course_file():
    os.makedirs("text", exist_ok=True)

    if not os.path.exists(COURSE_FILE):
        open(COURSE_FILE, "w").close()


def read_courses():
    ensure_course_file()
    courses = []

    with open(COURSE_FILE, "r") as file:
        for line in file:
            if line.strip():
                data = line.strip().split(",")

                if len(data) == 6:
                    courses.append(data)

    return courses


def save_courses(courses):
    with open(COURSE_FILE, "w") as file:
        for course in courses:
            file.write(",".join(course) + "\n")


def check_course_id(course_id, courses):
    for course in courses:
        if course[0].upper() == course_id.upper():
            return True

    return False


def get_course_id(courses, updating=False):
    while True:
        course_id = input("Enter Course ID: ").strip().upper()

        if course_id == "":
            print("Course ID cannot be empty.")

        elif "," in course_id:
            print("Commas are not allowed.")

        elif check_course_id(course_id, courses) and not updating:
            print("Course ID already exists. Please try again.")

        else:
            return course_id


def get_course_name():
    while True:
        course_name = input("Enter Course Name: ").strip()

        if course_name == "":
            print("Course Name cannot be empty.")

        elif "," in course_name:
            print("Commas are not allowed.")

        else:
            return course_name


def get_category():
    while True:
        category = input("Enter Course Category: ").strip()

        if category == "":
            print("Category cannot be empty.")

        elif "," in category:
            print("Commas are not allowed.")

        else:
            return category


def get_duration():
    while True:
        duration = input("Enter Course Duration (e.g. 4 weeks): ").strip()

        if duration == "":
            print("Duration cannot be empty.")

        elif "," in duration:
            print("Commas are not allowed.")

        else:
            return duration


def get_fee():
    while True:
        fee = input("Enter Course Fee: ").strip()

        try:
            if float(fee) < 0:
                print("Fee cannot be negative.")
            else:
                return fee
        except ValueError:
            print("Invalid fee. Please enter a number.")


def get_capacity():
    while True:
        capacity = input("Enter Course Capacity: ").strip()

        if capacity.isdigit() and int(capacity) > 0:
            return capacity

        print("Invalid capacity. Please enter a positive whole number.")


def display_course_details(course):
    print("---------------------------------")
    print("Course ID   :", course[0])
    print("Course Name :", course[1])
    print("Category    :", course[2])
    print("Duration    :", course[3])
    print("Fee         :", course[4])
    print("Capacity    :", course[5])
    print("---------------------------------")


def add_course():
    print("\n========== ADD COURSE ==========")

    courses = read_courses()
    course_id = get_course_id(courses)
    course_name = get_course_name()
    category = get_category()
    duration = get_duration()
    fee = get_fee()
    capacity = get_capacity()

    course = [course_id, course_name, category, duration, fee, capacity]
    courses.append(course)
    save_courses(courses)

    print("\nCourse Added Successfully!")
    display_course_details(course)


def display_courses():
    print("\n========== DISPLAY COURSES ==========")

    courses = read_courses()

    if not courses:
        print("No course records found.")
        return

    print("-" * 105)
    print("{:<15} {:<25} {:<18} {:<15} {:<12} {:<10}".format(
        "Course ID", "Course Name", "Category", "Duration", "Fee", "Capacity"
    ))
    print("-" * 105)

    for course in courses:
        print("{:<15} {:<25} {:<18} {:<15} {:<12} {:<10}".format(
            course[0], course[1][:24], course[2][:17],
            course[3][:14], course[4], course[5]
        ))

    print("-" * 105)


def update_course():
    print("\n========== UPDATE COURSE ==========")

    courses = read_courses()

    if not courses:
        print("No course records found.")
        return

    course_id = input("Enter Course ID to update: ").strip().upper()
    selected_course = None

    for course in courses:
        if course[0].upper() == course_id:
            selected_course = course
            break

    if selected_course is None:
        print("Course ID does not exist.")
        return

    print("\nCurrent Course Details")
    display_course_details(selected_course)
    print("Press Enter to keep the current value.")

    new_name = input("Enter New Course Name: ").strip()
    if new_name != "" and "," not in new_name:
        selected_course[1] = new_name
    elif "," in new_name:
        print("Commas are not allowed. Keeping the old Course Name.")

    new_category = input("Enter New Category: ").strip()
    if new_category != "" and "," not in new_category:
        selected_course[2] = new_category
    elif "," in new_category:
        print("Commas are not allowed. Keeping the old Category.")

    new_duration = input("Enter New Duration: ").strip()
    if new_duration != "" and "," not in new_duration:
        selected_course[3] = new_duration
    elif "," in new_duration:
        print("Commas are not allowed. Keeping the old Duration.")

    new_fee = input("Enter New Fee: ").strip()
    if new_fee != "":
        try:
            if float(new_fee) >= 0:
                selected_course[4] = new_fee
            else:
                print("Fee cannot be negative. Keeping the old Fee.")
        except ValueError:
            print("Invalid fee. Keeping the old Fee.")

    new_capacity = input("Enter New Capacity: ").strip()
    if new_capacity != "":
        if new_capacity.isdigit() and int(new_capacity) > 0:
            selected_course[5] = new_capacity
        else:
            print("Invalid capacity. Keeping the old Capacity.")

    save_courses(courses)

    print("\nCourse Updated Successfully!")
    display_course_details(selected_course)


def delete_course():
    print("\n========== DELETE COURSE ==========")

    courses = read_courses()

    if not courses:
        print("No course records found.")
        return

    course_id = input("Enter Course ID to delete: ").strip().upper()
    selected_course = None

    for course in courses:
        if course[0].upper() == course_id:
            selected_course = course
            break

    if selected_course is None:
        print("Course ID does not exist.")
        return

    print("\nCourse Details")
    display_course_details(selected_course)

    confirmation = input(
        "Are you sure you want to delete this course? (Y/N): "
    ).strip().upper()

    if confirmation == "Y":
        courses.remove(selected_course)
        save_courses(courses)
        print("Course Deleted Successfully!")
    else:
        print("Delete operation cancelled.")


def run_menu():
    ensure_course_file()

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_course()

        elif choice == "2":
            display_courses()

        elif choice == "3":
            update_course()

        elif choice == "4":
            delete_course()

        elif choice == "5":
            break


if __name__ == "__main__":
    run_menu()

