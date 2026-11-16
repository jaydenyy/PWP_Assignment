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

def enroll_member():
    while True:
        memberID = input("Enter Member ID: ")
        if memberID in ("1"):
            courseID = input("Enter Course ID: ")
            if courseID in ("1"):
                print("Enrolling Member")
                return
            print("Invalid ID. Please enter a valid ID.")



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