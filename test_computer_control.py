from computer_control import execute_intent

print("Computer Control Test")
print("1 = Open Calculator")
print("2 = Exit")

while True:
    choice = input("Enter choice: ").strip()

    if choice == "1":
        success, message = execute_intent("OPEN_CALCULATOR")
        print(message)

    elif choice == "2":
        print("Test stopped.")
        break

    else:
        print("Invalid choice.")