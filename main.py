import members
import courses
import enrollments
import resources


def display_main_menu():
    """Display the main menu."""
    print("\n" + "=" * 45)
    print("DOODLE COMMUNITY LEARNING HUB SYSTEM")
    print("=" * 45)
    print("1. Member Management")
    print("2. Course Management")
    print("3. Enrollment Management")
    print("4. Learning Resource Management")
    print("5. Exit")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")


def main():
    """Run the main system and open the selected management module."""
    while True:
        display_main_menu()
        choice = get_menu_choice()

        if choice == "1":
            members.run_menu()

        elif choice == "2":
            courses.run_menu()

        elif choice == "3":
            enrollments.run_menu()

        elif choice == "4":
            resources.run_menu()

        elif choice == "5":
            print("\nThank you for using Doodle Community Learning Hub System.")
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()