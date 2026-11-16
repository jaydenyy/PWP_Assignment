import os
from datetime import date


def display_menu():
    print("\n" + "=" * 45)
    print("DOODLE ENROLMENT MANAGEMENT")
    print("=" * 45)
    print("1. Enrol Member")
    print("2. Display and Search Enrolments")
    print("3. Update Enrolments")
    print("4. Delete Enrolments")
    print("5. Back to Main Menu")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")


def enrol_member():
    print("\n========== ENROL MEMBER ==========")

    if not os.path.exists("text/members.txt") or not os.path.exists("text/courses.txt"):
        print("Error: Member or Course data file not found.")
        return

    while True:
        memberID = input("Enter Member ID: ").strip().upper()
        member_exists = False

        with open("text/members.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if data[0] == memberID:
                    member_exists = True
                    break

        if member_exists:
            break

        print("Member ID does not exist. Please try again.")

    while True:
        courseID = input("Enter Course ID: ").strip().upper()
        course_exists = False

        with open("text/courses.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == courseID:
                    course_exists = True
                    break
        if course_exists:
            break
        print("Course ID does not exist. Please try again.")

    enrollmentID = "E001"

    if os.path.exists("text/enrollments.txt"):
        with open("text/enrollments.txt", "r") as file:
            count = sum(1 for line in file if line.strip())

        enrollmentID = "E" + str(count + 1).zfill(3)

    enrollmentDate = date.today().strftime("%Y-%m-%d")

    status = "Active"

    with open("text/enrollments.txt", "a") as file:
        file.write(f"{enrollmentID},{memberID},{courseID},{enrollmentDate},{status}\n")

    print("\nEnrollment Successful!")
    print("---------------------------------")
    print("Enrollment ID :", enrollmentID)
    print("Member ID     :", memberID)
    print("Course ID     :", courseID)
    print("Date          :", enrollmentDate)
    print("Status        :", status)
    print("---------------------------------")


def run_menu():
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            enrol_member()

        elif choice == "2":
            display_enrolments()

        elif choice == "3":
            update_enrolments()

        elif choice == "4":
            delete_enrolments()

        elif choice == "5":
            break
