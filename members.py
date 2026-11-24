import csv
import os
import re
from datetime import datetime

DATA_FILE = "members.txt"
ENROLMENT_FILE = "enrollments.txt"

ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9_-]{1,14}")
CONTACT_PATTERN = re.compile(r"^\+?[0-9][0-9 \-]{5,19}$")
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
COMMA_ERROR = "Commas (,) are not allowed because they would break the CSV file."

MENU = """
=============================================
   MEMBER MANAGEMENT SYSTEM 
=============================================
   1. Register a new member
   2. View / search members
   3. Update a member
   4. Delete a member
   0. Exit
============================================="""
    
def load_members(path=DATA_FILE):
    members = []
    if not os.path.exists(path):
        return members

    with open(path,newline="",encoding="utf-8-sig") as fh:
        for line_no,row in enumerate(csv.reader(fh),start=1):
           if not row or all(cell.strip() == "" for cell in row):
              continue
           if line_no == 1 and row[0].strip().lower()in ("members id","memberid","id"):
              continue
           if len(row)<6:
               print(f"[Warning]Line{line_no}is incomplete and was skipped.")
               continue
           mid,name,age,contact,email,start=[cell.strip()for cell in row[:6]]
           try:
               age_value=int(age)
           except ValueError:
               print(f"[Warning]Line{line_no}has an invalid age was skipped.")
               continue
           members.append({
                "id":mid,
                "name":name,
                "age":age_value,
                "contact":contact,
                "email":email,
                "start":start,
                 })
        return members

def save_members(members,path=DATA_FILE):
    tmp_path = path+".tmp"
    with open(tmp_path,"w",newline="",encoding="ut1f-8")as fh:
        writer = csv.writer(fh)
        for m in members:
            writer.writerow([m["id"],m["name"],m["age"],m["contact"],m["email"],m["start"]])
    os.replace(tmp_path,path)

def find_member(members,member_id):
    key = member_id.strip().lower()
    for m in members:
        if m["id"].lower() == key:
            return m
    return None

def next_member_id(members):
    highest=0
    for m in members:
        match = re.fullmatch(r"M(\d+)",m["id"],re.IGNORECASE)
        if match:
            highest = max(highest,int(match.group(1)))
    return f"M{highest+1:03d}"

def confirm(prompt):
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y","yes"):
                return True
            if answer in ("n","no",""):
                return False
            print("  !Please answer y or n.")

def read_text(label,current=None):
    suffix = f"[{current}]"if  current is not None else ""
    while True:
        raw = input(f"{label}{suffix}:").strip()
        if raw =="":
            if current is not None:
                return current
            print(" ! This field cannot be empty.")
            continue
        if "," in raw:
            print(f" !{COMMA_ERROR}")
            continue
        return raw

def read_age(current=None):
    suffix = f"[{current}]"if current is not None else ""
    while True:
        raw = input(f"Age 5-120{suffix}:").strip()
        if raw == ""and current is not None:
             return current
        try:
            value = int(raw)
        except ValueError:
            print(" ! Please enter a whole number, e.g. 24.")
            continue
        if not 5 <= value <= 120:
            print(" Age must be between 5 and 120.")
            continue
        return value

def read_contact(current=None):
    suffix = f"[{current}]" if current is not None else ""
    while True:
        raw = input(f"Contact number (e.g. 012-3456789){suffix}:")
        if raw == "" and current is not None:
             return current
        digits = re.sub(r"\D","",raw)
        if not CONTACT_PATTERN.match(raw) or not 7<= len(digits) <= 15:
            print(" !Please enter a valid phone number, e.g. 012-3456789.")
            continue
        return raw

def read_email(current=None):
    suffix = f"[{current}]" if current is not None else""
    while True:
        raw = input(f"Email address (e.g. name@gmail.com ){suffix}:").strip()
        if raw == "" and current is not None:
            return current
        if not EMAIL_PATTERN.match(raw):
            print(" ! Please enter a valid email address, e.g. name@mail.com")
            continue
        return raw

def read_data(label, current=None):
    today = datetime.today().strftime("%Y-%m-%d")
    suffix = f"[{current}]" if current is not None else ""
    while True:
        raw = input(f"{label}(YYYY-MM-DD, e.g. {today}{suffix}:").strip()
        if raw == "" and current is not None:
            return current
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            print("  ! Invalid date. Please use YYYY-MM-DD, e.g. 2026-01-15.")
            continue
        if not 1900 <= parsed.year <= 2100:
            print("  ! The year looks wrong. Please check again.")
            continue
        return parsed.strftime("%Y-%m-%d")

def print_table(members):
    if not members:
        print("\n (No members found.)")
        return

    headers = ["Member Id","Name","Age","Contact","Email","Start Date"]
    rows = [[m["id"],m["name"],str(m["age"]),m["contact"],m["email"],m["start"]]for m in members]
    widths = [max([len(headers[i])]+[len(r[i])for r in rows]) for i in range(len(headers))]
    border = "+" + "+".join("-"*(w+2)for w in widths)+"+"

    def format_row(cells):
        return "| " + " | ".join(cell.ljust(widths[i])for u,cell in enumerate(cells))+"|"
    print(border)
    print(format_row(headers))
    print(border)
    for r in rows:
        print(format_row(r))
        print(border)

def print_members_detail(member):
    print(f" Member ID :{member['id']}")
    print(f" Name :{member['name']}")
    print(f" Age :{member['age']}")
    print(f" Contact:{member['contact']}")
    print(f" Email :{member['email']}")
    print(f" Start Date:{member['start']}")

def active_enrolment_for(member_id, path=ENROLMENT_FILE):
    if not os.path.exists(path):
        return 0
    total = 0
    try:
        with open(path,newline="",encoding="utf-8-sig") as fh:
            for row in csv.reader(fh):
                if (len(row) >= 5
                     and row[1].strip().lower() == member_id.lower()
                      and row[4].strip().lower() == "active"):
                   total += 1
    except OSError:
        return 0
    return total

def prompt_existing_member(members,prompt):
    while True:
        raw = input(prompt).strip()
        if raw == "0":
            print("Cancelled.")
            return None
        if raw == "":
            print(" ! Please enter a Member ID.")
            continue
        member = find_member(members, raw)
        if member is None:
            print(f" ! Member ID{raw.upper()}was not found. Please try again.")
            continue
        return member

def add_member(members):
    print("\n--- Register a new member ---")
    suggestion = next_member_id(members)

    while True:
        raw = input(f"Member ID (press Enter to use {suggestion},0 to cancel):").strip()
        if raw == "0":
            print("Add cancelled.")
            return
        member_id = (raw or suggestion).upper()
        if not ID_PATTERN.fullmatch(member_id):
            print(" ! Use 2-15 letters/digits, e.g. M004 ( no spaces or commas).")
            continue
        if find_member(members, member_id):
            print(f" ! Member ID{member_id} already exists. Please choose another ID.")
            continue
        break

    member = {
        "id":member_id,
        "name":read_text("Name"),
        "age":read_age(),
        "contact":read_contact(),
        "email":read_email(),
        "start":read_data("Membership Start Date"),
    }

    print("\nNew member to be saved:")
    print_members_detail(member)
    if not confirm("Save this member? (y/n):"):
        print("Add cancelled.")
        return

    members.append(member)
    save_members(members)
    print(f"Member{member_id} has been registered.")

def view_members(members):
    print("\n --- View / search members ---")
    keyword = input("Search by Member ID or name(press Enter to show all):").strip()

    if keyword:
        key = keyword.lower()
        results = [m for m in members
                   if key in m["id"].lower() or key in m["name"].lower()]
    else:
        results = list(members)

    print(f"\n{len(results)}member(s) found:")
    if results:
        print()
        print_table(results)
    else:
        print("\n (No members found.)")

def update_member(members):
    print("\n --- Update members ---")
    if not members:
        print("There are no members to update.")
        return

    member = prompt_existing_member(members, "Enter the Member ID to update(0 to cancel):")
    if member is None:
        return

    print("\nCurrent record:")
    print_members_detail(member)
    print("\nPress Enter to keep the current value.")

    updated = {
        "id":member["id"],
        "name":read_text("Name",member["name"]),
        "age":read_age(member["age"]),
        "contact":read_contact(member["contact"]),
        "email":read_email(member["email"]),
        "start":read_data("Membership start date",member["start"]),
    }

    if updated == member:
        print("No changes made.")
        return

    print("\nUpdated record:")
    print_members_detail(updated)
    if not confirm("Save these changes?(y/n):"):
        print("Updated Cancelled.")
        return

    member.update(updated)
    save_members(members)
    print(f"[OK]Member{member['id']}has been updated.")

def delete_member(members):
    print("\n --- Delete members ---")
    if not members:
        print("There are no members to delete.")
        return

    member = prompt_existing_member(members, "Enter the Member ID to delete:")
    if member is None:
        return

    print("\nRecord to delete:")
    print_members_detail(member)

    active = active_enrolment_for(member["id"])
    if active:
        print(f"\n WARNING:{active}active enrolment(s) in {ENROLMENT_FILE}"
              f"still belong to this member.")
        print("Delete the member will leave those records pointing to a missing member.")

    if not confirm(f"Delete member {member['id']}permanently?(y/n):"):
        print("Deleted Cancelled.")
        return

    members.remove(member)
    save_members(members)
    print(f"[OK] Member {member['id']}has been deleted.")

def main():
    print(MENU)
    members = load_members()
    print(f"Loaded {len(members)} member(s) from {os.path.abspath(DATA_FILE)}")

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            add_member(members)
        elif choice == "2":
            view_members(members)
        elif choice == "3":
            update_member(members)
        elif choice == "4":
            delete_member(members)
        else:
            print("  ! Invalid choice. Please enter 0, 1, 2, 3 or 4.")
        print(MENU)

if __name__ == "__main__":
    main()



