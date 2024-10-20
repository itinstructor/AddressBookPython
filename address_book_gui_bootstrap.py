"""
    Name: address_book_gui.py
    Author: William Loring
    Created: 01/05/22
    Tkinter version of MVC (Model View Controller) Address Book
    This is the view, the user interace
"""
from base64 import b64decode
# Import tkinter library
from tkinter import *
# python pip install ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# Database operations library
import db_operations
from address_book_png import icon_data_16
from address_book_png import icon_data_32


class AddressBook:
    def __init__(self):
        """
        Initialize the AddressBook class.

        This method creates a database controller object, 
        creates a table in the database if it doesn't exist,
        initializes the Tkinter GUI, lists the existing records,
        and starts the main Tkinter program loop.
        """
        # Create the database controller object
        # If the database doesn't exist, it is created
        self.db_op = db_operations.DBOperations("address_book.db")

        # The controller creates the table if it doesn't exist
        self.db_op.create_table()

        # Initialize Tkinter GUI
        self.init_gui()

        # List the existing records to show on startup
        self.fetch_all_records()

        # Start the main Tkinter program loop
        mainloop()

# --------------------------- INITIALIZE GUI  ---------------------------- #
    def init_gui(self):
        """
        Initialize the GUI of the Address Book application.

        This method creates the main window of the application,
        sets its properties, creates and grids the frames and widgets.
        """
        # Create main application root window
        self.root = ttk.Window(themename="darkly")

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Set window location on screen 400 pixels right 300 pixels down
        # The window size will change based on the controls
        self.root.geometry("+400+300")

        # Add icon to program title bar
        small_icon = PhotoImage(data=b64decode(icon_data_16))
        large_icon = PhotoImage(data=b64decode(icon_data_32))
        self.root.iconphoto(False, large_icon, small_icon)

        self.root.title("Address Book")
        self.root.resizable(False, False)

        # Create and grid all widgets
        self.create_frames()
        self.create_widgets()
        self.create_treeview()

# -------------------------- INSERT RECORD ------------------------------- #
    def insert_record(self):
        """Add new record to database"""
        # Clear status label
        self.lbl_status.configure(text="")

        # Get input from user
        first_name = self.entry_fname.get()
        last_name = self.entry_lname.get()
        phone = self.entry_phone.get()
        email = self.entry_email.get()

        # Ensure the user enters a complete record
        if not first_name or not last_name:
            self.lbl_status.configure(text="Please fill out all entries")
        else:
            try:
                # Insert record into database
                self.db_op.insert_record(first_name, last_name, phone, email)

                # Let the user know the add record was successful
                self.lbl_status.configure(
                    text=f"{first_name} {last_name} was successfully added."
                )
            except:
                self.lbl_status.configure(
                    text=f"Error"
                )

        # Clear the entry widgets
        self.clear_entry_widgets()

        # Display all records in treeview
        self.fetch_all_records()

        # Set focus to entry widget for next entry
        self.entry_fname.focus()

# ------------------------ FETCH ALL RECORDS ----------------------------- #
    def fetch_all_records(self):
        """List all records in database"""
        # Return a list of tuples from treeview
        items = self.tree.get_children()

        # Iterate through list to delete all items in the treeview
        for item in items:
            self.tree.delete(item)

        # Query to get all contacts
        # sorted by last name in desc (descending) order
        # Get all records as a list of tuples
        records = self.db_op.fetch_all_records()

        # Insert all records into tree
        # Unpack the records tuple into variables one item at a time
        try:
            for id, first_name, last_name, phone, email in records:
                self.tree.insert("", 0, text=id, values=(
                    id, first_name, last_name, phone, email)
                )
        except:
            pass

# ----------------------- ON TREE SELECT --------------------------------- #
    def on_tree_select(self, event):
        """When a record is selected, the values are inserted into
           the appropriate entry boxes for modification."""
        try:
            # Clear entry widgets
            self.clear_entry_widgets()

            # Get the selected (focus) item from the tree
            self.selected = self.tree.focus()

            # Get the values from the selected tree item if item is selected
            if self.selected != "":
                self.selected_values = self.tree.item(
                    self.selected, "values"
                )

                # Insert tree values into Entry widgets
                # to show the selected record
                self.entry_fname.insert(0, self.selected_values[1])
                self.entry_lname.insert(0, self.selected_values[2])
                self.entry_phone.insert(0, self.selected_values[3])
                self.entry_email.insert(0, self.selected_values[4])

            # Set focus on first name entry
            # If tree still has focus, will cause selected value errors
            self.entry_fname.focus()
        except Exception as e:
            print(e)

# ----------------------- UPDATE RECORD ---------------------------------- #
    def update_record(self):
        """Update the currently selected record from the info in the form"""
        try:
            # Get the id (Primary Key) from the selected tree item
            id = self.selected_values[0]

            # Get the modified data from the entry widgets
            first_name = self.entry_fname.get()
            last_name = self.entry_lname.get()
            phone = self.entry_phone.get()
            email = self.entry_email.get()

            # Execute query against SQLite database
            self.db_op.update_record(first_name, last_name, phone, email, id)

            # Clear entry widgets
            self.clear_entry_widgets()

            # Display all records in treeview
            self.fetch_all_records()

            # Give the user the status of the operation
            self.lbl_status.configure(
                text=f"{first_name} {last_name} was successfully updated.")

        except:
            self.lbl_status.configure(
                text="Please select a record to modify")

# ----------------------- DELETE RECORD ---------------------------------- #
    def delete_record(self):
        """Delete selected record from database"""
        try:
            # Clear status label
            self.lbl_status.configure(text="")

            # id is the first value in the
            # selected item/values in the treelist
            id = (self.selected_values[0])

            # Execute the query against the SQLite database
            self.db_op.delete_record(id)

            # Clear the Entry widgets
            self.clear_entry_widgets()

            # Set the focus
            self.entry_fname.focus()

            # List all records
            self.fetch_all_records()

            # Confirm to the user that the record was deleted
            status = f"{self.selected_values[1]} "
            status += f"{self.selected_values[2]} was successfully deleted."
            self.lbl_status.configure(text=status)

        except:
            self.lbl_status.configure(text="Select a record to delete")

# -------------------------- CREATE FRAMES --------------------------------#
    def create_frames(self):
        self.entry_frame = ttk.LabelFrame(
            self.root,
            text="Enter Contact Info",
            relief=GROOVE
        )
        self.operations_frame = ttk.LabelFrame(
            self.root,
            text="Record Operations",
            relief=GROOVE
        )
        self.treeview_frame = ttk.LabelFrame(
            self.root,
            text="Contact List",
            relief=GROOVE
        )
        # Grid the frames
        self.entry_frame.grid(row=0, column=0, sticky=NW)
        self.operations_frame.grid(row=0, column=1, sticky=N)
        self.treeview_frame.grid(row=1, column=0, columnspan=2, sticky=W)

# ------------------------- CREATE WIDGETS ------------------------------- #
    def create_widgets(self):
        # ------------------------ CREATE LABELS ------------------------- #
        self.lbl_first_name = ttk.Label(
            self.entry_frame, text="First Name:", anchor="e")
        self.lbl_last_name = ttk.Label(
            self.entry_frame, text="Last Name:", anchor="e")
        self.lbl_phone = ttk.Label(
            self.entry_frame, text="Phone:", anchor="e")
        self.lbl_email = ttk.Label(
            self.entry_frame, text="Email:", anchor="e")
        self.lbl_status = ttk.Label(self.entry_frame, text=" ", anchor="w")

        # -------------------- CREATE ENTRY BOXES ------------------------ #
        self.entry_fname = ttk.Entry(self.entry_frame, width=30)
        # Set focus for data entry
        self.entry_fname.focus_set()
        self.entry_lname = ttk.Entry(self.entry_frame, width=30)
        self.entry_phone = ttk.Entry(self.entry_frame, width=30)
        self.entry_email = ttk.Entry(self.entry_frame, width=30)

        # ------------------------ CREATE BUTTONS ------------------------ #
        self.btn_add = ttk.Button(
            self.operations_frame,
            text="Add",
            command=self.insert_record
        )
        self.btn_modify = ttk.Button(
            self.operations_frame,
            text="Update Selected",
            command=self.update_record
        )
        self.btn_delete = ttk.Button(
            self.operations_frame,
            text="Delete Selected",
            command=self.delete_record
        )
        self.btn_close = ttk.Button(
            self.operations_frame,
            text="Close",
            command=self.close
        )

        # ------------------------- GRID WIDGETS ------------------------- #
        self.lbl_first_name.grid(row=0, column=0)
        self.lbl_last_name.grid(row=1, column=0)
        self.lbl_phone.grid(row=2, column=0)
        self.lbl_email.grid(row=3, column=0)
        self.lbl_status.grid(row=4, column=0, columnspan=2)

        self.entry_fname.grid(row=0, column=1)
        self.entry_lname.grid(row=1, column=1)
        self.entry_phone.grid(row=2, column=1)
        self.entry_email.grid(row=3, column=1)

        self.btn_add.grid(row=0, column=0, sticky=EW)
        self.btn_modify.grid(row=1, column=0, sticky=EW)
        self.btn_delete.grid(row=2, column=0, sticky=EW)
        self.btn_close.grid(row=3, column=0, sticky=EW)

        # Set padding between frame and window
        self.entry_frame.grid_configure(padx=20, pady=(20))
        self.operations_frame.grid_configure(padx=20, pady=(20))
        # Even out the padding between frames, leave out y distance on top
        self.treeview_frame.grid_configure(padx=20, pady=(0, 20))

        # Set padding for all widgets inside the frame
        for widget in self.entry_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)
        for widget in self.treeview_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)
        for widget in self.operations_frame.winfo_children():
            widget.grid_configure(padx=7, pady=7)

# ------------------------- TREEVIEW AND SCROLLBAR ----------------------- #
    def create_treeview(self):
        """Setup tree view for record display"""

        # Define the columns for the treeview
        self.columns = "id", "first_name", "last_name", "phone", "email"

        # Create the Treeview widget
        self.tree = ttk.Treeview(
            self.treeview_frame,  # Parent frame that contains the treeview
            height=10,  # Number of rows visible in the treeview
            columns=self.columns,  # Database fields (columns) for the treeview
            # Style for the widget (optional, based on theme)
            style="Treeview",
            show="headings",  # Show only the column headings, without the root column
            selectmode="browse"  # Only one row can be selected at a time
        )

        # Set the width for each column in the treeview
        self.tree.column("id", width=40)
        self.tree.column("first_name", width=150)
        self.tree.column("last_name", width=150)
        self.tree.column("phone", width=175)
        self.tree.column("email", width=300)

        # Set up the column headings with sorting functionality
        # Text shown in the "id" column header
        self.tree.heading("id", text="ID", anchor=W,
                          # Sort by ID when clicked
                          command=lambda: self.sort_treeview("id", False)
                          )
        self.tree.heading("first_name", text="First Name", anchor=W,
                          command=lambda: self.sort_treeview(
                              "first_name", False)
                          )
        self.tree.heading("last_name", text="Last Name", anchor=W,
                          command=lambda: self.sort_treeview(
                              "last_name", False)
                          )
        self.tree.heading("phone", text="Phone", anchor=W,
                          command=lambda: self.sort_treeview("phone", False)
                          )
        self.tree.heading(
            "email",
            text="Email",
            anchor=W,
            command=lambda: self.sort_treeview("email", False)
        )

        # Place the treeview widget in the grid at row 0, column 0
        self.tree.grid(row=0, column=0)

        # Create a vertical scrollbar for the treeview
        self.scrollbar = ttk.Scrollbar(
            self.treeview_frame,  # Parent frame for the scrollbar
            orient="vertical",  # Scrollbar orientation
            command=self.tree.yview  # Command to scroll the treeview vertically
        )

        # Configure the treeview to work with the scrollbar
        self.tree.configure(yscroll=self.scrollbar.set)

        # Place the scrollbar next to the treeview (right side) and make it stretch vertically
        self.scrollbar.grid(row=0, column=1, sticky="sn")

        # Bind the selection event to a handler
        # This will trigger when a row is selected in the treeview
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

# ----------------------- SORT TREEVIEW ---------------------------------- #
    def sort_treeview(self, column, descending):
        # Function to sort the Treeview by the specified column.

        # Extract the data from the Treeview.
        # For each item in the Treeview, get the value associated with the
        # specified column. This creates a list of tuples, where each
        # tuple contains the column value and the item (Treeview row).
        data = [(self.tree.set(item, column), item)
                for item in self.tree.get_children('')]

        # Sort the list of tuples based on the column values.
        # 'reverse=descending' determines the order of sorting
        # (ascending or descending).
        data.sort(reverse=descending)

        # Rearrange the items in the Treeview to reflect the sorted order.
        # 'enumerate' provides an index, which is used to set the
        # new position for each item.
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)

        # Update the column heading to allow toggling between
        # ascending and descending order for the next click.
        self.tree.heading(
            column, command=lambda: self.sort_treeview(column, not descending)
        )

# --------------------- CLEAR ENTRY WIDGETS ------------------------------ #
    def clear_entry_widgets(self):
        # Clear entry widgets, set focus to name entry widget
        self.entry_fname.delete(0, END)
        self.entry_lname.delete(0, END)
        self.entry_phone.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_fname.focus()

# -------------------------- CLOSE PROGRAM ------------------------------- #
    def close(self):
        self.root.destroy()


# ----------------------- START PROGRAM ---------------------------------- #
address_book = AddressBook()
