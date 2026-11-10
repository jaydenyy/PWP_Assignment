def display_menu():
    print("\n" + "=" * 45)
    print("DOODLE ENROLLMENT MANAGEMENT")
    print("=" * 45)
    print("1. Enroll Member")
    print("2. Display and Search Enrollments")
    print("3. Update Enrollments")
    print("4. Delete Enrollments")
    print("5. Back to Main Menu")
    print("=" * 45)

def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")

def run_menu():
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            enroll_member()

        elif choice == "2":
            display_enrollments()

        elif choice == "3":
            update_enrollments()

        elif choice == "4":
            delete_enrollments()

        elif choice == "5":
            break