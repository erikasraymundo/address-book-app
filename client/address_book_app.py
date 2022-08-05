import json
import os
from address_book_api_client import AddressBookApiClient
from address_book_validations import AddressBookValidations

validations = AddressBookValidations()
address_book_api_client = AddressBookApiClient()


def clear_screen():
    os.system("cls")


def display_menu():

    clear_screen()
    print()
    print_header()
    print("\nMenu:\n" +
          "[1] - Display all the addresses\n" +
          "[2] - Search an entry\n" +
          "[3] - Add New Entry\n" +
          "[4] - Edit an Entry\n" +
          "[5] - Delete an Entry\n" +
          "[6] - Exit app\n")

    while True:
        selection = input("User Selection: ")

        if selection == "1":
            clear_screen()
            print(str("-"*23).rjust(60))
            print("|  LIST OF ADDRESSES  |".rjust(60))
            print(str("-"*23).rjust(60))
            display_entries(address_book_api_client.get_address_book())
            return_to_menu()
            break

        elif selection == "2":
            clear_screen()
            print_header()
            print_title("Search an entry")
            search_entry_screen()
            return_to_menu()
            break

        elif selection == "3":
            add_entry_screen()
            return_to_menu()
            break

        elif selection == "4":
            update_entry_screen()
            return_to_menu()
            break

        elif selection == "5":
            delete_entry_screen()
            return_to_menu()
            break

        elif selection == "6":
            print("Thank you for using the app!")
            break
            # exit()

        else:
            print(">> Error: Select from the choices only.")


def return_to_menu():
    input("\nPress enter to return to menu...")
    display_menu()


def display_entries(entries):
    index = 1

    print("-" * 105)
    print("{} | {} | {} | {} | {}".format(
          "NO.".center(3),
          "NAME".center(25),
          "HOME ADDRESS".center(28),
          "CONTACT NO.".center(11),
          "EMAIL ADDRESS".center(25)))

    print("-" * 105)

    for entry in entries:
        def checkIfNone(input): return input if input != "" else "--"
        print("{} | {} | {} | {} | {}".format(
            str(index).center(3),
            str(entry.get("name")).rjust(25),
            str(entry.get("address")).rjust(28),
            str(checkIfNone(entry.get("contact_number"))).rjust(11),
            str(checkIfNone(entry.get("email"))).rjust(25)))
        index = index + 1

    print("-" * 105)


def add_entry_screen():
    clear_screen()
    print_header()
    print_title("Adding an Entry")

    while True:
        try:
            name = input("Enter name: ")
            address = input("Enter address: ")
            email = input("Enter email (optional): ")
            contact = input("Enter contact number (optional): ")

            if validations.validate_inputs(name, address, contact, email):

                entry = {"name": name,
                         "address": address, "email": email, "contact_number": contact}

                address_book_api_client.add_new_address_book(entry)
                print("\n>> SUCCESS: Entry has been added!")
                break
        except:
            print(">> Error: The program encountered an unknown error, try again later.")


def search_entry_screen():
    query = input("Enter a name you want to search: ")
    results = address_book_api_client.search_entries(query)

    if len(results) <= 0:
        print(">> No entries founds.")
    else:
        print(">> Search Results for '{}':".format(query))
        display_entries(results)

    return results


def search_entry_to_modify(results, operation):
    if len(results) > 0:

        while True:
            try:
                index = int(input("Enter entry no. to {}: ".format(operation)))
                if index >= 1 and index <= len(results):
                    return results[index-1]
                else:
                    print(
                        ">> Error: That entry #no doesn't exist, please only choose from {} - {}.".format(1, len(results)))
            except:
                print(">> Error: Numbers only.")
    else:
        print("No entries founds.")

    return None


def update_entry_screen():
    clear_screen()
    print_header()
    print_title("Update an Entry")

    results = search_entry_screen()
    if len(results) > 1:
        record_to_edit = search_entry_to_modify(results, "edit")
    elif len(results) == 1:
        record_to_edit = results[0]
    else:
        record_to_edit = None

    if record_to_edit != None:

        print("\nYou are editing {}...\n".format(record_to_edit.get("name")))
        
        def get_user_input(
            input, default): return input if input != "" else default

        while True:
            name = record_to_edit.get("name")
            address = record_to_edit.get("address")
            contact = record_to_edit.get("contact_number")
            email = record_to_edit.get("email")

            name = get_user_input(
                input("Enter new name [{}]: ".format(name)), name)
            address = get_user_input(
                input("Enter new address [{}]: ".format(address)), address)
            contact = get_user_input(
                input("Enter new contact [{}]: ".format(contact)), contact)
            email = get_user_input(
                input("Enter new email [{}]: ".format(email)), email)

            if validations.validate_inputs(name, address, contact, email):
                record_to_edit["name"] = name
                record_to_edit["address"] = address
                record_to_edit["contact_number"] = contact
                record_to_edit["email"] = email
                id = record_to_edit["id"]

                address_book_api_client.update_entry(id, record_to_edit)
                print("\n>> SUCCESS: The entry has been updated successfully!")
                break


def delete_entry_screen():
    clear_screen()
    print_header()
    print_title("Deleting an Entry")

    results = search_entry_screen()
    if len(results) > 1:
        entry_to_delete = search_entry_to_modify(results, "delete")
        print("You are deleting {}...".format(entry_to_delete["name"]))
    elif len(results) == 1:
        entry_to_delete = results[0]
        print("You are deleting {}...".format(entry_to_delete["name"]))
    else:
        entry_to_delete = None

    if entry_to_delete != None:
        def confirm_func(a, b, c): return a.lower() == b or a.lower() == c

        while True:
            try:
                confirm_choice = input(
                    "Are you sure you want to delete entry? Y - yes | N - no: ")
                if confirm_func(confirm_choice, "y", "yes"):
                    address_book_api_client.delete_entry(entry_to_delete["id"])
                    print("\n>> SUCCESS: The entry has been deleted!")
                    break
                elif confirm_func(confirm_choice, "n", "no"):
                    print(">> You cancelled the delete operation.")
                    break
                else:
                    print(">> Error: Invalid choice.")
            except:
                print(">> Error: Try again later.")


def print_header():
    print("Address Book App")


def print_title(title):
    print("** {} **\n".format(title))


display_menu()
