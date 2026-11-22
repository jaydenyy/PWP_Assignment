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


