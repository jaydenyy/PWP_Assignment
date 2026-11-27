import os

DATA_FOLDER = "text"
COURSE_FILE = os.path.join(DATA_FOLDER, "courses.txt")


def display_menu():
    print("\\n" + "=" * 45)
    print("DOODLE COURSE MANAGEMENT")
    print("=" * 45)
    print("1. Add Course")
    print("2. Display and Search Courses")
    print("3. Update Courses")
    print("4. Delete Courses")
    print("5. Back to Main Menu")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("Invalid choice. Please enter a number from 1 to 5.")


def read_courses():
    if not os.path.exists(COURSE_FILE):
        open(COURSE_FILE, "w").close()
    with open(COURSE_FILE, "r") as file:
        records = [line.strip().split(",") for line in file if line.strip()]
    return [record for record in records if len(record) == 5]


def save_courses(courses):
    with open(COURSE_FILE, "w") as file:
        for course in courses:
            file.write(",".join(course) + "\\n")


def generate_course_id():
    highest_number = 0
    for course in read_courses():
        course_id = course[0].strip().upper()
        if course_id.startswith("C") and course_id[1:].isdigit():
            highest_number = max(highest_number, int(course_id[1:]))
    return "C" + str(highest_number + 1).zfill(3)


def get_valid_course_name():
    while True:
        name = input("Enter Course Name: ").strip()
        if name == "":
            print("Course Name cannot be empty.")
        elif "," in name:
            print("Course Name cannot contain commas.")
        else:
            return name


def get_valid_duration():
    while True:
        duration = input("Enter Course Duration (e.g. 12 Weeks): ").strip()
        if duration == "":
            print("Course Duration cannot be empty.")
        elif "," in duration:
            print("Course Duration cannot contain commas.")
        else:
            return duration


def get_valid_fee():
    while True:
        fee = input("Enter Course Fee: ").strip()
        try:
            if float(fee) >= 0:
                return fee
            print("Fee cannot be negative.")
        except ValueError:
            print("Invalid fee. Please enter a number.")


def get_valid_capacity():
    while True:
        capacity = input("Enter Course Capacity: ").strip()
        if capacity.isdigit() and int(capacity) > 0:
            return capacity
        print("Capacity must be a positive whole number.")


def add_course():
    print("\\n========== ADD COURSE ==========")
    courses = read_courses()
    course_id = generate_course_id()
    course_name = get_valid_course_name()
    duration = get_valid_duration()
    fee = get_valid_fee()
    capacity = get_valid_capacity()

    course = [course_id, course_name, duration, fee, capacity]
    courses.append(course)
    save_courses(courses)

    print("\\nCourse Added Successfully!")
    print("---------------------------------")
    print("Course ID   :", course_id)
    print("Course Name :", course_name)
    print("Duration    :", duration)
    print("Fee         :", fee)
    print("Capacity    :", capacity)
    print("---------------------------------")


def display_courses():
    while True:
        print("\\n========== DISPLAY COURSES ==========")
        print("1. Display All Courses")
        print("2. Search by Course ID")
        print("3. Search by Course Name")
        print("4. Back")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "4":
            return
        if choice not in ("1", "2", "3"):
            print("Invalid choice.")
            continue

        courses = read_courses()
        if not courses:
            print("No course records found.")
            continue

        if choice == "2":
            search_id = input("Enter Course ID: ").strip().upper()
            courses = [c for c in courses if c[0].upper() == search_id]
        elif choice == "3":
            search_name = input("Enter Course Name: ").strip().lower()
            courses = [c for c in courses if search_name in c[1].lower()]

        if not courses:
            print("No matching courses found.")
            continue

        print("\\n" + "=" * 85)
        print(f"{'Course ID':<15}{'Course Name':<25}{'Duration':<15}{'Fee':<15}{'Capacity':<15}")
        print("=" * 85)
        for course in courses:
            print(f"{course[0]:<15}{course[1]:<25}{course[2]:<15}{course[3]:<15}{course[4]:<15}")
        print("=" * 85)


def update_courses():
    while True:
        print("\\n========== UPDATE COURSES ==========")
        course_id = input("Enter Course ID (or 0 to go back): ").strip().upper()
        if course_id == "0":
            return

        courses = read_courses()
        found = False

        for course in courses:
            if course[0].upper() == course_id:
                found = True
                print("\\nCourse Found")
                print("Course ID   :", course[0])
                print("Course Name :", course[1])
                print("Duration    :", course[2])
                print("Fee         :", course[3])
                print("Capacity    :", course[4])
                print("\\nAvailable Fields:")
                print("1. Course Name")
                print("2. Duration")
                print("3. Fee")
                print("4. Capacity")
                print("0. Cancel")
                choice = input("Select the field to update (0-4): ").strip()

                if choice == "1":
                    course[1] = get_valid_course_name()
                elif choice == "2":
                    course[2] = get_valid_duration()
                elif choice == "3":
                    course[3] = get_valid_fee()
                elif choice == "4":
                    course[4] = get_valid_capacity()
                else:
                    print("Update cancelled.")
                    break

                save_courses(courses)
                print("Course updated successfully!")
                break

        if not found:
            print("Course ID not found.")


def delete_courses():
    while True:
        print("\\n========== DELETE COURSES ==========")
        course_id = input("Enter Course ID (or 0 to go back): ").strip().upper()
        if course_id == "0":
            return

        courses = read_courses()
        found = False

        for course in courses:
            if course[0].upper() == course_id:
                found = True
                print("\\nCourse Found")
                print("Course ID   :", course[0])
                print("Course Name :", course[1])
                print("Duration    :", course[2])
                print("Fee         :", course[3])
                print("Capacity    :", course[4])
                confirm = input("\\nAre you sure you want to delete this course? (Y/N): ").strip().upper()

                if confirm == "Y":
                    courses.remove(course)
                    save_courses(courses)
                    print("Course deleted successfully!")
                else:
                    print("Deletion cancelled.")
                break

        if not found:
            print("Course ID not found.")


def run_menu():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    if not os.path.exists(COURSE_FILE):
        open(COURSE_FILE, "w").close()

    while True:
        display_menu()
        choice = get_menu_choice()
        if choice == "1":
            add_course()
        elif choice == "2":
            display_courses()
        elif choice == "3":
            update_courses()
        elif choice == "4":
            delete_courses()
        elif choice == "5":
            print("Returning to Main Menu...")
            break


if __name__ == "__main__":
    run_menu()
