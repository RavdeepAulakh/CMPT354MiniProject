import sqlite3

# Connect to the database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()


# Function to create a new member account
def create_member(name, address, email, phone, membership_type):
    try:
        cursor.execute(
            "INSERT INTO Member (Name, Address, Email, Phone, MembershipType) VALUES (?, ?, ?, ?, ?)",
            (name, address, email, phone, membership_type),
        )
        conn.commit()
        print("New member account created successfully!")
        return cursor.lastrowid  # Return the new MemberID
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return None


def prompt_create_member():
    print("\nEnter member details:")
    name = input("Name: ")
    address = input("Address: ")
    email = input("Email: ")
    phone = input("Phone: ")
    print("\nMembership Types: Basic, Premium")
    membership_type = input("Membership Type: ")

    member_id = create_member(name, address, email, phone, membership_type)

    if member_id:
        member_info = {
            "member_id": member_id,
            "name": name,
            "address": address,
            "email": email,
            "phone": phone,
            "membership_type": membership_type,
        }
        return member_info
    return None


def login_member(member_id=None):
    if member_id is None:
        member_id = input("Enter your Member ID: ")

    cursor.execute(
        """
        SELECT MemberID, Name, Address, Email, Phone, MembershipType 
        FROM Member 
        WHERE MemberID = ?""",
        (member_id,),
    )

    member = cursor.fetchone()

    if member:
        member_info = {
            "member_id": member[0],
            "name": member[1],
            "address": member[2],
            "email": member[3],
            "phone": member[4],
            "membership_type": member[5],
        }
        print(f"Welcome back, {member_info['name']}!")
        return member_info
    else:
        print("Member not found.")
        return None


def find_item(title=None):
    if title == None:
        title = input("Enter item title or keyword: ")

    cursor.execute("SELECT * FROM Item WHERE Title LIKE ?", ("%" + title + "%",))
    items = cursor.fetchall()

    if items:
        print("\nFound items:")
        for item in items:
            print(
                f"ID: {item[0]}, Title: {item[1]}, Type: {item[2]}, Genre: {item[3]}, Available: {bool(item[4])}"
            )
    else:
        print("No matching items found.")
    return items


def donate_item(title=None, item_type=None, bookInfo=None, artist=None, genre=None):
    if title == None and item_type == None:
        title = input("Enter item title: ")
        item_type = input("Enter item type (Book/DVD/CD or Other): ").strip().lower()

    if item_type in ["book", "dvd", "cd"]:
        cursor.execute(
            "INSERT INTO Item (Title, Type, Genre, Availability, DateAdded) VALUES (?, ?, ?, 1, date('now'))",
            (title, item_type.upper(), None),
        )
        item_id = cursor.lastrowid  # Get the generated ItemID
        print(f"Generated ItemID: {item_id}")  # Debugging

        if item_type == "book":
            if not bookInfo:
                isbn = input("Enter ISBN: ")
                author = input("Enter author: ")
                publisher = input("Enter publisher (optional): ")
                year = input("Enter year of publication: ")
                edition = input("Enter edition (optional): ")
            else:
                isbn = bookInfo.get("ISBN")
                author = bookInfo.get("Author")
                publisher = bookInfo.get("Publisher", "")
                year = bookInfo.get("Year")
                edition = bookInfo.get("Edition", "")

            # Check if the book already exists
            cursor.execute("SELECT ISBN FROM Book WHERE ISBN = ?", (isbn,))
            if cursor.fetchone():
                print("Error: This book already exists in the database.")
                return 1

            # Check if the ItemID already exists in the Book table
            cursor.execute("SELECT ItemID FROM Book WHERE ItemID = ?", (item_id,))
            if cursor.fetchone():
                print("Error: This ItemID already exists in the Book table.")
                return 1

            # Insert into the Book table
            cursor.execute(
                "INSERT INTO Book (ISBN, Title, Author, Publisher, Year, Edition, ItemID) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (isbn, title, author, publisher, year, edition, item_id),
            )

        else:  # DVD or CD
            if artist == None:
                artist = input("Enter artist (optional): ")
            cursor.execute(
                "INSERT INTO Multimedia (Title, Artist, Type, Genre, ItemID) VALUES (?, ?, ?, ?, ?)",
                (title, artist, item_type.upper(), None, item_id),
            )

    else:
        if not genre:
            genre = input("Enter item genre: ")
        cursor.execute(
            "INSERT INTO Item (Title, Type, Genre, Availability) VALUES (?, ?, ?, 1)",
            (title, "OTHER", genre),
        )

    conn.commit()
    print("Thank you for your donation!")
    return 0


def borrow_item(member_id=None, item_id=None):
    if member_id == None and item_id == None:
        member_id = input("Enter your Member ID: ")
        item_id = input("Enter Item ID to borrow: ")

    cursor.execute("SELECT Availability FROM Item WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()

    if item and item[0] == 1:  # Item is available
        cursor.execute(
            "INSERT INTO Borrow (MemberID, ItemID, BorrowDate, DueDate) VALUES (?, ?, date('now'), date('now', '+14 days'))",
            (member_id, item_id),
        )
        cursor.execute("UPDATE Item SET Availability = 0 WHERE ItemID = ?", (item_id,))
        conn.commit()
        print("Item borrowed successfully!")
        return 0
    else:
        print("Item is not available.")
        return 1


def return_item(member_id=None, item_id=None):
    if not member_id:
        member_id = "enter your member id: "

    if item_id == None:
        item_id = input("Enter Borrow ID: ")

    cursor.execute(
        "SELECT ItemID FROM Borrow WHERE ItemID = ? AND MemberID = ?",
        (item_id, member_id),
    )
    item = cursor.fetchone()

    if item:
        cursor.execute(
            "UPDATE Borrow SET ReturnDate = date('now') WHERE ItemID = ?",
            (item_id,),
        )
        cursor.execute("UPDATE Item SET Availability = 1 WHERE ItemID = ?", (item[0],))
        conn.commit()
        print("Item returned successfully!")
        return 0
    else:
        print("Invalid Borrow ID.")
        return 1


def show_borrowed_items(member_id):
    cursor.execute(
        """
        SELECT i.ItemID, i.Title, i.Type, b.BorrowDate, b.DueDate 
        FROM Item i 
        JOIN Borrow b ON i.ItemID = b.ItemID 
        WHERE b.MemberID = ? AND b.ReturnDate IS NULL
    """,
        (member_id,),
    )

    items = cursor.fetchall()
    if items:
        print("\nYour borrowed items:")
        for item in items:
            print(f"ID: {item[0]}, Title: {item[1]}, Type: {item[2]}")
            print(f"Borrowed: {item[3]}, Due: {item[4]}")
    else:
        print("You have no items currently borrowed.")
    return items


def show_fines(member_id):
    cursor.execute(
        """
        SELECT f.Amount, f.DueDate, f.PaidStatus 
        FROM Fine f  
        WHERE f.MemberID = ?
    """,
        (member_id,),
    )

    fines = cursor.fetchall()
    if fines:
        print("\nYour fines:")
        for fine in fines:
            print(
                f"Amount: ${fine[0]}, Due Date: {fine[1]}, Paid: {'Yes' if fine[2] == '1' else 'No'}"
            )
    else:
        print("You have no fines.")
    return fines


def show_registered_events(member_id):
    cursor.execute(
        """
        SELECT e.EventID, e.Name, e.Date, e.Type, e.Time, e.AudienceType 
        FROM Event e 
        JOIN Attends a ON e.EventID = a.EventID 
        WHERE a.MemberID = ?
    """,
        (member_id,),
    )

    events = cursor.fetchall()
    if events:
        print("\nYour registered events:")
        for event in events:
            print(f"ID: {event[0]}, Name: {event[1]}")
            print(f"Date: {event[2]}, Type: {event[3]}")
            print(f"Time: {event[4]}, Audience: {event[5]}")
    else:
        print("You have no upcoming registered events.")
    return events


def login_screen():
    # Log in or Sign Up
    user_method = input("Enter 1 to log in\nEnter 2 to sign up\n: ")
    if user_method == "1":
        result = login_member()
    elif user_method == "2":
        result = prompt_create_member()
    else:
        print("Invalid option")
        result = None

    # if result:
    #     print("\nUser Details:")
    #     for key, value in result.items():
    #         print(f"{key}: {value}")

    return result

    # Function to find an event


def find_event():
    cursor.execute("SELECT * FROM Event")
    events = cursor.fetchall()

    if events:
        print("\nUpcoming Events:")
        for event in events:
            print(
                f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}"
            )
    else:
        print("No events found.")
    return events


def register_event(event_id=None, member_id=None):
    if event_id == None or member_id == None:
        event_id = input("Enter Event ID: ")
        member_id = input("Enter your Member ID: ")

    try:
        cursor.execute("SELECT * FROM Event WHERE EventID = ?", (event_id,))
        event = cursor.fetchone()
        if event is None:
            print("Error: Event ID does not exist.")
            return 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0

    try:
        cursor.execute(
            "INSERT INTO Attends (EventID, MemberID) VALUES (?, ?)",
            (event_id, member_id),
        )
        conn.commit()
        print("Event registration successful!")
    except sqlite3.IntegrityError:
        print("Already registered")
    return 0


def volunteer(member_id=None, contact_details=None):
    if not member_id:
        member_id = input("Enter your Member ID: ")
    role = "Volunteer"
    # Optionally, add contact details or any other required fields for the Personnel table
    if not contact_details:
        contact_details = input("Enter your contact details (optional): ")
    try:
        cursor.execute(
            "INSERT INTO Personnel (Name, Role, ContactDetails) SELECT Name, ?, ? FROM Member WHERE MemberID = ?",
            (role, contact_details, member_id),
        )
        conn.commit()
        print("Thank you for volunteering!")
    except sqlite3.IntegrityError:
        print("Already a volunteer!")
    return 0


def view_books():
    try:
        cursor.execute("SELECT * FROM Book")
        books = cursor.fetchall()

        if books:
            print("\nBooks in the database:")
            for book in books:
                print(
                    f"ISBN: {book[0]}, Title: {book[1]}, Author: {book[2]}, "
                    f"Publisher: {book[3]}, Year: {book[4]}, Edition: {book[5]}, ItemID: {book[6]}"
                )
        else:
            print("No books found in the database.")
    except Exception as e:
        print(f"Error: {e}")
