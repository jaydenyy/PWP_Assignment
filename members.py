import csv
import os
DATA_FILE = "members.txt"
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
def main():
    print(MENU)
    while True:
        choice = input("\nEnter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        if choice in ("1","2","3","4"):
            print(f"[TODO]Option{choice}is not ready yet.")
        else:
            print(" ! Invalid choice. Please enter 0,1,2,3 or 4.")
        print(MENU)

if __name__ == "__main__":
    main()

def load_members(path=DATA_FILE):
    members = []
    if not os.path.exists(path):
        return members

with open(path,newlines="",encoding="ult-8-sig")
    as fh:
    for line_no,row in
enumerate(csv.reader(fh),start=1):
    if not row or all(cell.strip() == "" for cell in row):
        continue
    if line_no == 1 and row[0].strip().lower()in ("members id","memberid","id"):
        continue
mid,name,age,contact,email,start = [cell.strip()for cell in row[:6]]
    try:
        age_value = int(age)



