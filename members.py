import os
from datetime import date


DATA_FOLDER = "text"
MEMBER_FILE = os.path.join(DATA_FOLDER, "members.txt")
ENROLMENT_FILE = os.path.join(DATA_FOLDER, "enrolments.txt")


def display_menu():
    print("\n" + "=" * 45)
    print("MEMBER MANAGEMENT")
    print("=" * 45)
    print("1. Register Member")
    print("2. Display and Search Members")
    print("3. Update Members")
    print("4. Delete Members")
    print("5. Back to Main Menu")
    print("=" * 45)


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-5): ").strip()

        if choice in ("1", "2", "3", "4", "5"):
            return choice

        print("Invalid choice. Please enter a number from 1 to 5.")

def get_valid_name():
    while True:
        name = input("Enter Name: ").strip()

        if name == "":
            print("Name cannot be empty.")
        elif "," in name:
            print("Name cannot contain commas.")
        else:
            return name


def get_valid_age():
    while True:
        text = input("Enter Age: ").strip()

        if text.isdigit():
            age = int(text)

            if 5 <= age <= 120:
                return text

            print("Age must be between 5 and 120.")
        else:
            print("Age must be a whole number.")


def get_valid_contact():
    while True:
        text = input("Enter Contact Number (e.g. 012-3456789): ").strip()

        digits = "".join(c for c in text if c.isdigit())
        allowed = all(c.isdigit() or c in " -+" for c in text)

        if allowed and 7 <= len(digits) <= 15:
            return text

        print("Invalid contact number. Use 7-15 digits, e.g. 012-3456789.")


def get_valid_email():
    while True:
        text = input("Enter Email (e.g. name@mail.com): ").strip()

        if "," not in text and " " not in text and text.count("@") == 1:
            user, domain = text.split("@")

            if user != "" and "." in domain and not domain.startswith(".") and not domain.endswith("."):
                return text

        print("Invalid email address, e.g. name@mail.com.")


def get_valid_start_date():
    while True:
        text = input("Enter Membership Start Date (YYYY-MM-DD, blank = today): ").strip()

        if text == "":
            return str(date.today())

        try:
            date.fromisoformat(text)
            return text
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD, e.g. 2026-01-15.")

def generate_member_id():
    highest = 0

    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE, "r") as file:
            for line in file:
                data = line.strip().replace("\ufeff", "").split(",")

                if data[0].startswith("M") and data[0][1:].isdigit():
                    highest = max(highest, int(data[0][1:]))

    return "M" + str(highest + 1).zfill(3)


def member_exists(memberID):
    if not os.path.exists(MEMBER_FILE):
        return False

    with open(MEMBER_FILE, "r") as file:
        for line in file:
            data = line.strip().replace("\ufeff", "").split(",")

            if data[0] == memberID:
                return True

    return False


def count_active_enrolments(memberID):
    if not os.path.exists(ENROLMENT_FILE):
        return 0

    total = 0

    with open(ENROLMENT_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")

            if len(data) == 5:
                if data[1] == memberID and data[4].strip().lower() == "active":
                    total += 1

    return total

def register_member():
    print("\n========== REGISTER MEMBER ==========")

    if not os.path.exists(MEMBER_FILE):
        open(MEMBER_FILE, "w").close()
        print("Members file not found. A new one has been created.")

    memberID = generate_member_id()

    while member_exists(memberID):
        memberID = "M" + str(int(memberID[1:]) + 1).zfill(3)

    name = get_valid_name()
    age = get_valid_age()
    contact = get_valid_contact()
    email = get_valid_email()
    startDate = get_valid_start_date()

    with open(MEMBER_FILE, "a") as file:
        file.write(f"{memberID},{name},{age},{contact},{email},{startDate}\n")

    print("\nRegistration Successful!")
    print("---------------------------------")
    print("Member ID   :", memberID)
    print("Name        :", name)
    print("Age         :", age)
    print("Contact     :", contact)
    print("Email       :", email)
    print("Start Date  :", startDate)
    print("---------------------------------")

def display_members():
    while True:
        print("\n========== DISPLAY MEMBERS ==========")
        print("1. Display All Members")
        print("2. Search by Member ID")
        print("3. Search by Name")
        print("4. Search by Email")
        print("5. Back")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "5":
            return

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice.")
            continue

        try:
            with open(MEMBER_FILE, "r") as file:
                records = [line.strip().replace("\ufeff", "").split(",") for line in file if line.strip()]

            if not records:
                print("No member records found.")
                continue

            if choice == "2":
                searchID = input("Enter Member ID: ").strip().upper()
                records = [r for r in records if len(r) == 6 and r[0] == searchID]

            elif choice == "3":
                searchName = input("Enter Name: ").strip().lower()
                records = [r for r in records if len(r) == 6 and searchName in r[1].lower()]

            elif choice == "4":
                searchEmail = input("Enter Email: ").strip().lower()
                records = [r for r in records if len(r) == 6 and searchEmail in r[4].lower()]

            if not records:
                print("No matching members found.")
                continue

            print("\n" + "=" * 106)
            print(f"{'Member ID':<12}{'Name':<25}{'Age':<6}{'Contact':<18}{'Email':<30}{'Start Date':<15}")
            print("=" * 106)

            for r in records:
                print(f"{r[0]:<12}{r[1]:<25}{r[2]:<6}{r[3]:<18}{r[4]:<30}{r[5]:<15}")

            print("=" * 106)

        except FileNotFoundError:
            print("Members file not found.")
            return

def update_members():
    while True:
        print("\n========== UPDATE MEMBERS ==========")

        memberID = input("Enter Member ID (or 0 to go back): ").strip().upper()

        if memberID == "0":
            return

        try:
            with open(MEMBER_FILE, "r") as file:
                records = [line.strip().split(",") for line in file if line.strip()]

            found = False

            for r in records:
                if len(r) == 6 and r[0] == memberID:
                    found = True

                    print("\nMember Found")
                    print("Member ID :", r[0])
                    print("Name      :", r[1])
                    print("Age       :", r[2])
                    print("Contact   :", r[3])
                    print("Email     :", r[4])
                    print("Start Date:", r[5])

                    print("\nAvailable Fields:")
                    print("1. Name")
                    print("2. Age")
                    print("3. Contact Number")
                    print("4. Email")
                    print("5. Membership Start Date")
                    print("0. Cancel")

                    choice = input("Select the field to update (0-5): ").strip()

                    if choice == "1":
                        r[1] = get_valid_name()
                    elif choice == "2":
                        r[2] = get_valid_age()
                    elif choice == "3":
                        r[3] = get_valid_contact()
                    elif choice == "4":
                        r[4] = get_valid_email()
                    elif choice == "5":
                        r[5] = get_valid_start_date()
                    else:
                        print("Update cancelled.")
                        break

                    with open(MEMBER_FILE, "w") as file:
                        for record in records:
                            file.write(",".join(record) + "\n")

                    print("Member updated successfully!")
                    break

            if not found:
                print("Member ID not found.")

        except FileNotFoundError:
            print("Members file not found.")
            return

def delete_members():
    while True:
        print("\n========== DELETE MEMBERS ==========")

        memberID = input("Enter Member ID (or 0 to go back): ").strip().upper()

        if memberID == "0":
            return

        try:
            with open(MEMBER_FILE, "r") as file:
                records = [line.strip().replace("\ufeff", "").split(",") for line in file if line.strip()]

            found = False

            for r in records:
                if len(r) == 6 and r[0] == memberID:
                    found = True

                    print("\nMember Found")
                    print("Member ID :", r[0])
                    print("Name      :", r[1])
                    print("Age       :", r[2])
                    print("Contact   :", r[3])
                    print("Email     :", r[4])
                    print("Start Date:", r[5])

                    active = count_active_enrolments(memberID)

                    if active > 0:
                        print(f"\nWarning: this member has {active} active enrolment(s).")

                    confirm = input("\nAre you sure you want to delete this member? (Y/N): ").strip().upper()

                    if confirm == "Y":
                        records.remove(r)

                        with open(MEMBER_FILE, "w") as file:
                            for record in records:
                                file.write(",".join(record) + "\n")

                        print("Member deleted successfully!")

                    else:
                        print("Deletion cancelled.")

                    break

            if not found:
                print("Member ID not found.")

        except FileNotFoundError:
            print("Members file not found.")
            return

def run_menu():
    os.makedirs(DATA_FOLDER, exist_ok=True)

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            register_member()

        elif choice == "2":
            display_members()

        elif choice == "3":
            update_members()

        elif choice == "4":
            delete_members()

        elif choice == "5":
            break


if __name__ == "__main__":
    run_menu()