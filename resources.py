import os

RESOURCE_FILE = "text/resources.txt"


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

                if len(data) == 5:
                    resources.append(data)

    return resources


def save_resources(resources):
    with open(RESOURCE_FILE, "w") as file:
        for resource in resources:
            file.write(",".join(resource) + "\n")


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value == "":
            print("This field cannot be empty.")
        elif "," in value:
            print("Commas are not allowed.")
        else:
            return value


def get_quantity():
    while True:
        quantity = input("Enter Quantity: ").strip()

        try:
            quantity = int(quantity)

            if quantity < 0:
                print("Quantity cannot be negative.")
            else:
                return str(quantity)

        except ValueError:
            print("Invalid quantity. Please enter a whole number.")


def get_availability():
    while True:
        status = input(
            "Enter Availability (Available/Unavailable): "
        ).strip().title()

        if status in ("Available", "Unavailable"):
            return status

        print("Invalid status. Please enter Available or Unavailable.")


def generate_resource_id(resources):
    highest_number = 0

    for resource in resources:
        resource_id = resource[0]

        if resource_id.startswith("R") and resource_id[1:].isdigit():
            number = int(resource_id[1:])

            if number > highest_number:
                highest_number = number

    return "R" + str(highest_number + 1).zfill(3)


def add_resource():
    print("\n========== ADD RESOURCE ==========")

    resources = read_resources()

    resource_id = generate_resource_id(resources)

    resource_name = get_non_empty_input("Enter Resource Name: ")
    resource_type = get_non_empty_input("Enter Resource Type/Category: ")
    quantity = get_quantity()
    availability = get_availability()

    resource = [
        resource_id,
        resource_name,
        resource_type,
        quantity,
        availability
    ]

    resources.append(resource)
    save_resources(resources)

    print("\nResource Added Successfully!")
    print("---------------------------------")
    print("Resource ID  :", resource_id)
    print("Resource Name:", resource_name)
    print("Type         :", resource_type)
    print("Quantity     :", quantity)
    print("Availability :", availability)
    print("---------------------------------")


def display_resources():
    print("\n========== DISPLAY RESOURCES ==========")

    resources = read_resources()

    if not resources:
        print("No resource records found.")
        return

    print("-" * 85)
    print("{:<10} {:<22} {:<18} {:<12} {:<15}".format(
        "ID", "Resource Name", "Type", "Quantity", "Availability"
    ))
    print("-" * 85)

    for resource in resources:
        print("{:<10} {:<22} {:<18} {:<12} {:<15}".format(
            resource[0],
            resource[1][:21],
            resource[2][:17],
            resource[3],
            resource[4]
        ))

    print("-" * 85)

    search_resources(resources)


def search_resources(resources):
    print("\n========== SEARCH RESOURCES ==========")
    print("1. Search by Resource ID")
    print("2. Search by Resource Name")
    print("3. Search by Resource Type")
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

        elif choice == "2" and keyword in resource[1].lower():
            found.append(resource)

        elif choice == "3" and keyword in resource[2].lower():
            found.append(resource)

    if found:
        print("\nSearch Results:")

        for resource in found:
            print("---------------------------------")
            print("Resource ID  :", resource[0])
            print("Resource Name:", resource[1])
            print("Type         :", resource[2])
            print("Quantity     :", resource[3])
            print("Availability :", resource[4])
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
        if resource[0].upper() == resource_id:
            selected_resource = resource
            break

    if selected_resource is None:
        print("Resource ID does not exist.")
        return

    print("\nCurrent Resource Details")
    print("---------------------------------")
    print("Resource ID  :", selected_resource[0])
    print("Resource Name:", selected_resource[1])
    print("Type         :", selected_resource[2])
    print("Quantity     :", selected_resource[3])
    print("Availability :", selected_resource[4])
    print("---------------------------------")

    print("Press Enter to keep the current value.")

    new_name = input("Enter New Resource Name: ").strip()

    while "," in new_name:
        print("Commas are not allowed.")
        new_name = input("Enter New Resource Name: ").strip()

    if new_name != "":
        selected_resource[1] = new_name

    new_type = input("Enter New Resource Type: ").strip()

    while "," in new_type:
        print("Commas are not allowed.")
        new_type = input("Enter New Resource Type: ").strip()

    if new_type != "":
        selected_resource[2] = new_type

    while True:
        new_quantity = input("Enter New Quantity: ").strip()

        if new_quantity == "":
            break

        try:
            quantity = int(new_quantity)

            if quantity < 0:
                print("Quantity cannot be negative.")
            else:
                selected_resource[3] = str(quantity)
                break

        except ValueError:
            print("Invalid quantity. Please enter a whole number.")

    while True:
        new_status = input(
            "Enter New Availability (Available/Unavailable): "
        ).strip().title()

        if new_status == "":
            break

        elif new_status in ("Available", "Unavailable"):
            selected_resource[4] = new_status
            break

        else:
            print("Invalid availability status.")

    save_resources(resources)

    print("\nResource Updated Successfully!")


def delete_resource():
    print("\n========== DELETE RESOURCE ==========")

    resources = read_resources()

    if not resources:
        print("No resource records found.")
        return

    resource_id = input("Enter Resource ID to delete: ").strip().upper()

    selected_resource = None

    for resource in resources:
        if resource[0].upper() == resource_id:
            selected_resource = resource
            break

    if selected_resource is None:
        print("Resource ID does not exist.")
        return

    print("\nResource Details")
    print("---------------------------------")
    print("Resource ID  :", selected_resource[0])
    print("Resource Name:", selected_resource[1])
    print("Type         :", selected_resource[2])
    print("Quantity     :", selected_resource[3])
    print("Availability :", selected_resource[4])
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
