import pyperclip

def generate_and_copy_text():
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        text = "hello1"
    elif choice == "2":
        text = "hello2"
    else:
        text = "Invalid choice"
    
    print(text)
    pyperclip.copy(text)
    print("Text copied to clipboard!")
