from DatabaseFunctions import *
from time import sleep


def ask_help(choice=None):
    # List the available options
    print("\nHelp Options:")
    print("1. Help with borrowing an item")
    print("2. Help with returning an item")
    print("3. Help with donating an item")
    print("4. Help with finding an event")
    print("5. Help with registering for an event")
    print("6. Help with volunteering")

    # Ask the user to choose a help option
    if not choice:
        choice = input("Enter the number of the help option you want explained: ")

    # Provide an explanation based on the choice
    if choice == "1":
        print("\nHelp with borrowing an item:")
        print(
            "To borrow an item, you need to find the item in the library and check its availability. If available, you can borrow it for 14 days."
        )
    elif choice == "2":
        print("\nHelp with returning an item:")
        print(
            "To return an item, you need the Borrow ID and the system will automatically update the item status to 'available'."
        )
    elif choice == "3":
        print("\nHelp with donating an item:")
        print(
            "You can donate an item by providing its title, type (e.g., book, DVD, or CD), and genre. The item will be added to the library collection."
        )
    elif choice == "4":
        print("\nHelp with finding an event:")
        print(
            "You can search for upcoming library events and see the event details, including the name, date, and location."
        )
    elif choice == "5":
        print("\nHelp with registering for an event:")
        print(
            "To register for an event, you need to choose an event and then register with your member ID to attend it."
        )
    elif choice == "6":
        print("\nHelp with volunteering:")
        print(
            "You can volunteer for the library by entering your member ID and optionally providing contact details. Your role will be set as 'Volunteer'."
        )
    else:
        print("Invalid option. Please choose a valid help option.")


def options_menu():
    print("\nLibrary Management System")
    print("1. Find an item")
    print("2. Borrow an item")
    print("3. Return an item")
    print("4. Donate an item")
    print("5. Find an event")
    print("6. Register for an event")
    print("7. Volunteer for the library")
    print("8. Ask for help")
    print("9. View my borrowed items")
    print("10. View my registered events")
    print("11. Show my fines")
    print("12. Exit")

    choice = input("\nEnter your choice: ")
    return choice


def main():
    # Log in or Sign Up
    userDetails = login_screen()

    member_id = userDetails.get("member_id")

    # show_borrowed_items(member_id=member_id)

    show_fines(member_id=member_id)

    while True:
        print(("\n\n" + "=" * 100))
        print(f"Logged in as: {userDetails.get("name")}  ||  Member ID: {member_id}")

        choice = options_menu()

        match choice:
            case "1":
                find_item(title=input("Enter title or press <Enter> to see all: "))
            case "2":
                borrow_item(
                    member_id=member_id,
                    item_id=input(
                        "Enter the item ID of what you would like to borrow: "
                    ),
                )
            case "3":
                show_borrowed_items(member_id=member_id)

                return_item(
                    member_id=member_id,
                    item_id=input("Enter the ID of the Item you wish to return: "),
                )
            case "4":
                donate_item()
            case "5":
                find_event()
            case "6":
                find_event()

                show_registered_events(member_id=member_id)

                register_event(
                    event_id=input(
                        "\nEnter the ID of the Event you with to register for: "
                    ),
                    member_id=member_id,
                )
            case "7":
                volunteer(member_id=member_id)
            case "8":
                ask_help()
            case "9":
                show_borrowed_items(member_id)
            case "10":
                show_registered_events(member_id)
            case "11":
                show_fines(member_id=member_id)
            case "12":
                print("Goodbye!")
                break
            case _:
                print("Not a Valid option")
        input("\nPress enter to continue")


if __name__ == "__main__":
    main()
