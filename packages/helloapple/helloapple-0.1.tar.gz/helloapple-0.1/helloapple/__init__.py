import pyperclip

def greet_and_copy():
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        message = "hello1"
    elif choice == '2':
        message = "hello2"
    else:
        message = "Invalid choice"

    print(message)
    pyperclip.copy(message)

greet_and_copy()
