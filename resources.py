
import os


def display_menu():
    print("\n" + "=" * 45)
    print("DOODLE RESOURCE MANAGEMENT")
    print("=" * 45)
    print("1. Add Resource")
    print("2. Display and Search Resources")
    print("3. Update Resources")
    print("4. Delete Resources")
    print("5. Back to Main Menu")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")


def add_resource():
    print("\n========== ADD RESOURCE ==========")

    if not os.path.exists("text/courses.txt"):
        print("Error: Course data file not found.")
        return

    if not os.path.exists("text/resources.txt"):
        open("text/resources.txt", "w").close()

    while True:
        courseID = input("Enter Course ID: ").strip().upper()
        course_exists = False

        if courseID == "":
            print("Course ID cannot be empty.")
            continue

        with open("text/courses.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if data[0].upper() == courseID:
                    course_exists = True
                    break

        if course_exists:
            break

        print("Course ID does not exist. Please try again.")

    resourceID = "R001"

    with open("text/resources.txt", "r") as file:
        records = [line.strip().split(",") for line in file if line.strip()]

    highest_number = 0

    for record in records:
        if len(record) == 4:
            if record[1].startswith("R") and record[1][1:].isdigit():
                number = int(record[1][1:])

                if number > highest_number:
                    highest_number = number

    resourceID = "R" + str(highest_number + 1).zfill(3)

    while True:
        resourceName = input("Enter Resource Name: ").strip()

        if resourceName == "":
            print("Resource Name cannot be empty.")

        elif "," in resourceName:
            print("Commas are not allowed.")

        else:
            break

    while True:
        available = input("Is the resource available? (Yes/No): ").strip().title()

        if available in ("Yes", "No"):
            break

        print("Invalid input. Please enter Yes or No.")

    with open("text/resources.txt", "a") as file:
        file.write(f"{courseID},{resourceID},{resourceName},{available}\n")

    print("\nResource Added Successfully!")
    print("---------------------------------")
    print("Course ID    :", courseID)
    print("Resource ID  :", resourceID)
    print("Resource Name:", resourceName)
    print("Available    :", available)
    print("---------------------------------")


def display_resources():
    while True:
        print("\n========== DISPLAY RESOURCES ==========")
        print("1. Display All Resources")
        print("2. Search by Resource ID")
        print("3. Search by Course ID")
        print("4. Search by Resource Name")
        print("5. Back")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "5":
            return

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice.")
            continue

        try:
            with open("text/resources.txt", "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            if not records:
                print("No resource records found.")
                continue

            if choice == "2":
                searchID = input("Enter Resource ID: ").strip().upper()
                records = [r for r in records if r[1].upper() == searchID]

            elif choice == "3":
                searchID = input("Enter Course ID: ").strip().upper()
                records = [r for r in records if r[0].upper() == searchID]

            elif choice == "4":
                searchName = input("Enter Resource Name: ").strip().lower()
                records = [r for r in records if searchName in r[2].lower()]

            if not records:
                print("No matching resources found.")
                continue

            print("\n" + "=" * 85)
            print(f"{'Course ID':<15}{'Resource ID':<15}{'Resource Name':<35}{'Available':<15}")
            print("=" * 85)

            for r in records:
                if len(r) == 4:
                    print(f"{r[0]:<15}{r[1]:<15}{r[2]:<35}{r[3]:<15}")

            print("=" * 85)

        except FileNotFoundError:
            print("Resources file not found.")
            return


def update_resources():

    while True:
        print("\n========== UPDATE RESOURCES ==========")

        resourceID = input("Enter Resource ID (or 0 to go back): ").strip().upper()

        if resourceID == "0":
            return

        try:
            with open("text/resources.txt", "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            found = False

            for r in records:
                if len(r) == 4 and r[1].upper() == resourceID:
                    found = True

                    print("\nResource Found")
                    print("Course ID:", r[0])
                    print("Resource ID:", r[1])
                    print("Resource Name:", r[2])
                    print("Current Availability:", r[3])

                    print("\nPress Enter to keep the current value.")

                    newCourseID = input("Enter New Course ID: ").strip().upper()

                    if newCourseID != "":
                        course_exists = False

                        if os.path.exists("text/courses.txt"):
                            with open("text/courses.txt", "r") as courseFile:
                                for line in courseFile:
                                    data = line.strip().split(",")

                                    if data[0].upper() == newCourseID:
                                        course_exists = True
                                        break

                        if course_exists:
                            r[0] = newCourseID
                        else:
                            print("Course ID does not exist. Keeping old Course ID.")

                    newResourceName = input("Enter New Resource Name: ").strip()

                    while "," in newResourceName:
                        print("Commas are not allowed.")
                        newResourceName = input("Enter New Resource Name: ").strip()

                    if newResourceName != "":
                        r[2] = newResourceName

                    print("\nAvailable Options:")
                    print("1. Yes")
                    print("2. No")

                    while True:
                        choice = input("Select new availability (1-2) or press Enter to keep current: ").strip()

                        if choice == "":
                            break

                        elif choice == "1":
                            r[3] = "Yes"
                            break

                        elif choice == "2":
                            r[3] = "No"
                            break

                        else:
                            print("Invalid choice. Please enter 1 or 2.")

                    with open("text/resources.txt", "w") as file:
                        for record in records:
                            file.write(",".join(record) + "\n")

                    print("Resource updated successfully!")
                    break

            if not found:
                print("Resource ID not found.")

        except FileNotFoundError:
            print("Resources file not found.")
            return


def delete_resources():

    while True:
        print("\n========== DELETE RESOURCES ==========")

        resourceID = input("Enter Resource ID (or 0 to go back): ").strip().upper()

        if resourceID == "0":
            return

        try:
            with open("text/resources.txt", "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            found = False

            for r in records:
                if len(r) == 4 and r[1].upper() == resourceID:
                    found = True

                    print("\nResource Found")
                    print("Course ID:", r[0])
                    print("Resource ID:", r[1])
                    print("Resource Name:", r[2])
                    print("Available:", r[3])

                    confirm = input(
                        "\nAre you sure you want to delete this resource? (Y/N): "
                    ).strip().upper()

                    if confirm == "Y":
                        records.remove(r)

                        with open("text/resources.txt", "w") as file:
                            for record in records:
                                file.write(",".join(record) + "\n")

                        print("Resource deleted successfully!")

                    else:
                        print("Deletion cancelled.")

                    break

            if not found:
                print("Resource ID not found.")

        except FileNotFoundError:
            print("Resources file not found.")
            return


def run_menu():
    os.makedirs("text", exist_ok=True)

    if not os.path.exists("text/resources.txt"):
        open("text/resources.txt", "w").close()

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_resource()

        elif choice == "2":
            display_resources()

        elif choice == "3":
            update_resources()

        elif choice == "4":
            delete_resources()

        elif choice == "5":
            break


if __name__ == "__main__":
    run_menu()
