import sqlite3

# Connect to the database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Function to search for an item in the library
def find_item():
    title = input("Enter item title or keyword: ")
    cursor.execute("SELECT * FROM Item WHERE Title LIKE ?", ('%' + title + '%',))
    items = cursor.fetchall()
    
    if items:
        print("\nFound items:")
        for item in items:
            print(f"ID: {item[0]}, Title: {item[1]}, Type: {item[2]}, Genre: {item[3]}, Available: {bool(item[4])}")
    else:
        print("No matching items found.")

# Function to borrow an item
def borrow_item():
    member_id = input("Enter your Member ID: ")
    item_id = input("Enter Item ID to borrow: ")
    
    cursor.execute("SELECT Availability FROM Item WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    
    if item and item[0] == 1:  # Item is available
        cursor.execute("INSERT INTO Borrow (MemberID, ItemID, BorrowDate, DueDate) VALUES (?, ?, date('now'), date('now', '+14 days'))", (member_id, item_id))
        cursor.execute("UPDATE Item SET Availability = 0 WHERE ItemID = ?", (item_id,))
        conn.commit()
        print("Item borrowed successfully!")
    else:
        print("Item is not available.")

# Function to return an item
def return_item():
    borrow_id = input("Enter Borrow ID: ")
    cursor.execute("SELECT ItemID FROM Borrow WHERE BorrowID = ?", (borrow_id,))
    item = cursor.fetchone()

    if item:
        cursor.execute("UPDATE Borrow SET ReturnDate = date('now') WHERE BorrowID = ?", (borrow_id,))
        cursor.execute("UPDATE Item SET Availability = 1 WHERE ItemID = ?", (item[0],))
        conn.commit()
        print("Item returned successfully!")
    else:
        print("Invalid Borrow ID.")

# Function to donate an item
def donate_item():
    title = input("Enter item title: ")
    item_type = input("Enter item type (Book/DVD/CD): ")
    genre = input("Enter item genre: ")

    cursor.execute("INSERT INTO Item (Title, Type, Genre, Availability) VALUES (?, ?, ?, 1)", (title, item_type, genre))
    conn.commit()
    print("Thank you for your donation!")

# Function to find an event
def find_event():
    cursor.execute("SELECT * FROM Event")
    events = cursor.fetchall()

    if events:
        print("\nUpcoming Events:")
        for event in events:
            print(f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}")
    else:
        print("No events found.")

# Function to register for an event
def register_event():
    event_id = input("Enter Event ID: ")
    member_id = input("Enter your Member ID: ")

    cursor.execute("INSERT INTO Attends (EventID, MemberID) VALUES (?, ?)", (event_id, member_id))
    conn.commit()
    print("Event registration successful!")

# Function to volunteer
def volunteer():
    member_id = input("Enter your Member ID: ")
    hours = input("Enter number of hours you can volunteer: ")

    cursor.execute("INSERT INTO Volunteer (MemberID, Hours) VALUES (?, ?)", (member_id, hours))
    conn.commit()
    print("Thank you for volunteering!")

# Function to ask for help
def ask_help():
    member_id = input("Enter your Member ID: ")
    question = input("Describe your issue: ")

    cursor.execute("INSERT INTO HelpRequest (MemberID, Question) VALUES (?, ?)", (member_id, question))
    conn.commit()
    print("Your request has been submitted. A librarian will assist you shortly.")

# Main Menu
def main():
    while True:
        print("\nLibrary Management System")
        print("1. Find an item")
        print("2. Borrow an item")
        print("3. Return an item")
        print("4. Donate an item")
        print("5. Find an event")
        print("6. Register for an event")
        print("7. Volunteer for the library")
        print("8. Ask for help")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            find_item()
        elif choice == "2":
            borrow_item()
        elif choice == "3":
            return_item()
        elif choice == "4":
            donate_item()
        elif choice == "5":
            find_event()
        elif choice == "6":
            register_event()
        elif choice == "7":
            volunteer()
        elif choice == "8":
            ask_help()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
