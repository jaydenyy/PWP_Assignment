
import os

RESOURCE_FILE = "text/resources.txt"
COURSE_FILE = "text/courses.txt"


def display_menu():
    print("\n" + "=" * 45)
    print("DOODLE RESOURCE MANAGEMENT")
    print("=" * 45)
    print("1. Add Resource")
    print("2. Display and Search Resources")
    print("3. Update Resource")
    print("4. Delete Resource")
    print("5. Back to Main Menu")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")


def ensure_resource_file():
    os.makedirs("text", exist_ok=True)

    if not os.path.exists(RESOURCE_FILE):
        open(RESOURCE_FILE, "w").close()


def read_resources():
    ensure_resource_file()
    resources = []

    with open(RESOURCE_FILE, "r") as file:
        for line in file:
            if line.strip():
                data = line.strip().split(",")

                if len(data) == 4:
                    resources.append(data)

    return resources


def save_resources(resources):
    with open(RESOURCE_FILE, "w") as file:
        for resource in resources:
            file.write(",".join(resource) + "\n")


def check_course_id(course_id):
    if not os.path.exists(COURSE_FILE):
        return False

    with open(COURSE_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")

            if data and data[0].upper() == course_id.upper():
                return True

    return False


def get_course_id():
    while True:
        course_id = input("Enter Course ID: ").strip().upper()

        if course_id == "":
            print("Course ID cannot be empty.")

        elif "," in course_id:
            print("Commas are not allowed.")

        elif check_course_id(course_id):
            return course_id

        else:
            print("Course ID does not exist. Please try again.")


def get_resource_name():
    while True:
        resource_name = input("Enter Resource Name: ").strip()

        if resource_name == "":
            print("Resource Name cannot be empty.")

        elif "," in resource_name:
            print("Commas are not allowed.")

        else:
            return resource_name


def get_availability():
    while True:
        available = input("Is the resource available? (Yes/No): ").strip().title()

        if available in ("Yes", "No"):
            return available

        print("Invalid input. Please enter Yes or No.")


def generate_resource_id(resources):
    highest_number = 0

    for resource in resources:
        resource_id = resource[1]

        if resource_id.startswith("R") and resource_id[1:].isdigit():
            number = int(resource_id[1:])

            if number > highest_number:
                highest_number = number

    return "R" + str(highest_number + 1).zfill(3)


def add_resource():
    print("\n========== ADD RESOURCE ==========")

    if not os.path.exists(COURSE_FILE):
        print("Error: Course data file not found.")
        return

    resources = read_resources()

    course_id = get_course_id()
    resource_id = generate_resource_id(resources)
    resource_name = get_resource_name()
    available = get_availability()

    resource = [
        course_id,
        resource_id,
        resource_name,
        available
    ]

    resources.append(resource)
    save_resources(resources)

    print("\nResource Added Successfully!")
    print("---------------------------------")
    print("Course ID    :", course_id)
    print("Resource ID  :", resource_id)
    print("Resource Name:", resource_name)
    print("Available    :", available)
    print("---------------------------------")


def display_resources():
    print("\n========== DISPLAY RESOURCES ==========")

    resources = read_resources()

    if not resources:
        print("No resource records found.")
        return

    print("-" * 75)
    print("{:<15} {:<15} {:<25} {:<15}".format(
        "Course ID", "Resource ID", "Resource Name", "Available"
    ))
    print("-" * 75)

    for resource in resources:
        print("{:<15} {:<15} {:<25} {:<15}".format(
            resource[0],
            resource[1],
            resource[2][:24],
            resource[3]
        ))

    print("-" * 75)

    search_resources(resources)


def search_resources(resources):
    print("\n========== SEARCH RESOURCES ==========")
    print("1. Search by Course ID")
    print("2. Search by Resource ID")
    print("3. Search by Resource Name")
    print("4. Back")

    while True:
        choice = input("Enter your choice (1-4): ").strip()

        if choice in ("1", "2", "3", "4"):
            break

        print("Invalid choice. Please try again.")

    if choice == "4":
        return

    keyword = input("Enter search keyword: ").strip().lower()

    if keyword == "":
        print("Search keyword cannot be empty.")
        return

    found = []

    for resource in resources:

        if choice == "1" and keyword == resource[0].lower():
            found.append(resource)

        elif choice == "2" and keyword == resource[1].lower():
            found.append(resource)

        elif choice == "3" and keyword in resource[2].lower():
            found.append(resource)

    if found:
        print("\nSearch Results:")

        for resource in found:
            print("---------------------------------")
            print("Course ID    :", resource[0])
            print("Resource ID  :", resource[1])
            print("Resource Name:", resource[2])
            print("Available    :", resource[3])

    else:
        print("No matching resource found.")


def update_resource():
    print("\n========== UPDATE RESOURCE ==========")

    resources = read_resources()

    if not resources:
        print("No resource records found.")
        return

    resource_id = input("Enter Resource ID to update: ").strip().upper()

    selected_resource = None

    for resource in resources:
        if resource[1].upper() == resource_id:
            selected_resource = resource
            break

    if selected_resource is None:
        print("Resource ID does not exist.")
        return

    print("\nCurrent Resource Details")
    print("---------------------------------")
    print("Course ID    :", selected_resource[0])
    print("Resource ID  :", selected_resource[1])
    print("Resource Name:", selected_resource[2])
    print("Available    :", selected_resource[3])
    print("---------------------------------")

    print("Press Enter to keep the current value.")

    new_course_id = input("Enter New Course ID: ").strip().upper()

    if new_course_id != "":
        if check_course_id(new_course_id):
            selected_resource[0] = new_course_id
        else:
            print("Invalid Course ID. Keeping the old Course ID.")

    new_name = input("Enter New Resource Name: ").strip()

    while "," in new_name:
        print("Commas are not allowed.")
        new_name = input("Enter New Resource Name: ").strip()

    if new_name != "":
        selected_resource[2] = new_name

    while True:
        new_available = input(
            "Is the resource available? (Yes/No): "
        ).strip().title()

        if new_available == "":
            break

        elif new_available in ("Yes", "No"):
            selected_resource[3] = new_available
            break

        else:
            print("Please enter Yes or No.")

    save_resources(resources)

    print("\nResource Updated Successfully!")
    print("---------------------------------")
    print("Course ID    :", selected_resource[0])
    print("Resource ID  :", selected_resource[1])
    print("Resource Name:", selected_resource[2])
    print("Available    :", selected_resource[3])
    print("---------------------------------")


def delete_resource():
    print("\n========== DELETE RESOURCE ==========")

    resources = read_resources()

    if not resources:
        print("No resource records found.")
        return

    resource_id = input("Enter Resource ID to delete: ").strip().upper()

    selected_resource = None

    for resource in resources:
        if resource[1].upper() == resource_id:
            selected_resource = resource
            break

    if selected_resource is None:
        print("Resource ID does not exist.")
        return

    print("\nResource Details")
    print("---------------------------------")
    print("Course ID    :", selected_resource[0])
    print("Resource ID  :", selected_resource[1])
    print("Resource Name:", selected_resource[2])
    print("Available    :", selected_resource[3])
    print("---------------------------------")

    confirmation = input(
        "Are you sure you want to delete this resource? (Y/N): "
    ).strip().upper()

    if confirmation == "Y":
        resources.remove(selected_resource)
        save_resources(resources)

        print("Resource Deleted Successfully!")

    else:
        print("Delete operation cancelled.")


def run_menu():
    ensure_resource_file()

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_resource()

        elif choice == "2":
            display_resources()

        elif choice == "3":
            update_resource()

        elif choice == "4":
            delete_resource()

        elif choice == "5":
            print("Returning to Main Menu...")
            break


if __name__ == "__main__":
    run_menu()
