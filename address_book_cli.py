"""
    Name: address_book_cli5_delete.py
    Author: William Loring
    Created: 01/05/22
    Purpose: MVC Address book CLI with SQLite
    This is the View
"""
# pip install tabulate
import tabulate
# Import database controller library
import db_operations


class AddressBook:
    def __init__(self):
        # Create db_operations object
        # This creates database and table if not exists
        self.db_op = db_operations.DBOperations("address_book.db")
        self.db_op.create_table()
        # Print program title
        print("+-------------------------------+")
        print("|      Bill's Contact List      |")
        print("+-------------------------------+")

# ----------------------------- MENU ---------------------------------------#
    def menu(self):
        """Program menu"""
        USER_CHOICE = """
(C)reate contact
(R)etrieve contacts
(D)elete contact
(B)ackup database to SQL
(Q)uit
-->> """
        user_input = input(USER_CHOICE)
        # Convert input into lower case
        user_input = user_input.lower()
        # Menu loop while user does not input q
        while user_input != "q":

            # -------------- Insert contact record ------------------------#
            if user_input == "c":
                self.insert_record()
                self.fetch_all_records()

        # ----------------- RETRIEVE ALL RECORDS ------------------------- #
            elif user_input == "r":
                self.fetch_all_records()

        # ------------------- DELETE SELECTED RECORD --------------------- #
            elif user_input == "d":
                self.fetch_all_records()
                self.delete_record()
                self.fetch_all_records()

        # ---------------------- DATABASE DUMP --------------------------- #
            elif user_input == "b":
                self.db_op.database_dump()

            else:
                print("Unknown option. Please try again")

            # Get user input
            user_input = input(USER_CHOICE)
            # Convert input into lower case
            user_input = user_input.lower()

# -------------------------- INSERT RECORD --------------------------------#
    def insert_record(self):
        """Insert new record"""
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        phone = input("Enter phone: ")
        email = input("Enter email: ")
        # Call controller insert record method with arguments
        self.db_op.insert_record(
            first_name,
            last_name,
            phone,
            email
        )

# ------------------------- FETCH ALL RECORDS -----------------------------#
    def fetch_all_records(self):
        """Fetch all records"""
        # Call controller fetch all records method
        all_records = self.db_op.fetch_all_records()
        print("\nBill's Contact List")
        print()
        # Records are returned as a list of tuples
        # Use tablulate library to format the data nicely
        print(
            tabulate.tabulate(
                all_records,
                headers=["id", "First Name", "Last Name", "Phone", "Email"],
                tablefmt="psql"  # Table format
            )
        )

# ------------------------- DELETE RECORD ----------------------------------#
    def delete_record(self):
        """Delete selected record"""
        # Get primary key from user
        id = int(input("Enter contact id to delete: "))
        # Call controller delete record method with argument
        self.db_op.delete_record(id)


# ------------------------------ START PROGRAM -----------------------------#
address_book = AddressBook()
address_book.menu()
