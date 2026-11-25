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

    with open("text/enrolments.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")

            if len(data) == 5:
                if data[1] == memberID and data[2] == courseID and data[4] == "Active":
                    print("Member is already enrolled in this course.")
                    return

    enrollmentID = "E001"

    if os.path.exists("text/enrolments.txt"):
        with open("text/enrolments.txt", "r") as file:
            count = sum(1 for line in file if line.strip())

        enrollmentID = "E" + str(count + 1).zfill(3)

    enrollmentDate = date.today().strftime("%Y-%m-%d")

    status = "Active"

    with open("text/enrolments.txt", "a") as file:
        file.write(f"{enrollmentID},{memberID},{courseID},{enrollmentDate},{status}\n")

    print("Enrollment Successful!")
    print("Enrollment ID:", enrollmentID)

    print("\nEnrollment Successful!")
    print("---------------------------------")
    print("Enrollment ID :", enrollmentID)
    print("Member ID     :", memberID)
    print("Course ID     :", courseID)
    print("Date          :", enrollmentDate)
    print("Status        :", status)
    print("---------------------------------")

def display_enrolments():
    while True:
        print("\n========== DISPLAY ENROLMENTS ==========")
        print("1. Display All Enrolments")
        print("2. Search by Enrolment ID")
        print("3. Search by Member ID")
        print("4. Search by Course ID")
        print("5. Back")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "5":
            return

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice.")
            continue

        try:
            with open("text/enrolments.txt", "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            if not records:
                print("No enrolment records found.")
                continue

            if choice == "2":
                searchID = input("Enter Enrolment ID: ").strip().upper()
                records = [r for r in records if r[0] == searchID]

            elif choice == "3":
                searchID = input("Enter Member ID: ").strip().upper()
                records = [r for r in records if r[1] == searchID]

            elif choice == "4":
                searchID = input("Enter Course ID: ").strip().upper()
                records = [r for r in records if r[2] == searchID]

            if not records:
                print("No matching enrolments found.")
                continue

            print("\n" + "=" * 85)
            print(f"{'Enrolment ID':<15}{'Member ID':<15}{'Course ID':<15}{'Date':<20}{'Status':<15}")
            print("=" * 85)

            for r in records:
                print(f"{r[0]:<15}{r[1]:<15}{r[2]:<15}{r[3]:<20}{r[4]:<15}")

            print("=" * 85)

        except FileNotFoundError:
            print("Enrolments file not found.")
            return

def update_enrolments():

    while True:
        print("\n========== UPDATE ENROLMENTS ==========")

        enrollmentID = input("Enter Enrollment ID (or 0 to go back): ").strip().upper()

        if enrollmentID == "0":
            return

        try:
            with open("text/enrolments.txt", "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            found = False

            for r in records:
                if r[0] == enrollmentID:
                    found = True
                    print("\nEnrollment Found")
                    print("Member ID:", r[1])
                    print("Course ID:", r[2])
                    print("Current Status:", r[4])

                    print("\nAvailable Statuses:")
                    print("1. Active")
                    print("2. Completed")
                    print("3. Withdrawn")

                    choice = input("Select new status (1-3): ").strip()

                    if choice == "1":
                        r[4] = "Active"
                    elif choice == "2":
                        r[4] = "Completed"
                    elif choice == "3":
                        r[4] = "Withdrawn"
                    else:
                        print("Invalid choice.")
                        break

                    with open("text/enrolments.txt", "w") as file:
                        for record in records:
                            file.write(",".join(record) + "\n")

                    print("Enrollment updated successfully!")
                    break

            if not found:
                print("Enrollment ID not found.")

        except FileNotFoundError:
            print("Enrolments file not found.")
            return

def delete_enrolments():

    while True:
        print("\n========== DELETE ENROLMENTS ==========")

        enrollmentID = input("Enter Enrollment ID (or 0 to go back): ").strip().upper()

        if enrollmentID == "0":
            return

        try:
            with open("text/enrolments.txt", "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            found = False

            for r in records:
                if r[0] == enrollmentID:
                    found = True

                    print("\nEnrollment Found")
                    print("Enrollment ID:", r[0])
                    print("Member ID:", r[1])
                    print("Course ID:", r[2])
                    print("Date:", r[3])
                    print("Status:", r[4])

                    confirm = input("\nAre you sure you want to delete this enrollment? (Y/N): ").strip().upper()

                    if confirm == "Y":
                        records.remove(r)

                        with open("text/enrolments.txt", "w") as file:
                            for record in records:
                                file.write(",".join(record) + "\n")

                        print("Enrollment deleted successfully!")

                    else:
                        print("Deletion cancelled.")

                    break

            if not found:
                print("Enrollment ID not found.")

        except FileNotFoundError:
            print("Enrolments file not found.")
            return

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
