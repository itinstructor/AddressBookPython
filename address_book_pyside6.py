"""
    Name: address_book_qt.py
    PySide6 version of MVC Address Book
    This is the view, the user interface
    Claude AI was used to help convert from Tkinter version to PySide6
"""
# pip install pyside6
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTreeWidget, QTreeWidgetItem, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QImage
import sys
import base64
from address_book_png import icon_data_16
import db_operations


class AddressBook(QMainWindow):
    def __init__(self):
        """
        Initialize the AddressBook class.
        Creates a database controller object, creates a table if it doesn't exist,
        initializes the Qt GUI, and lists existing records.
        """
        super().__init__()

        try:
            # Create the database controller object
            self.db_op = db_operations.DBOperations("address_book.db")

            # The controller creates the table if it doesn't exist
            self.db_op.create_table()
        except Exception as e:
            QMessageBox.critical(
                self, "Database Error",
                f"Error initializing database: {e}")
            sys.exit(1)

        # Track current sort column and order
        self.sort_column = 0  # Default sort by ID
        self.sort_order = Qt.AscendingOrder

        # Initialize GUI
        self.init_gui()

        # List existing records
        self.fetch_all_records()

# ---------------------------- INIT GUI ---------------------------------- #
    def init_gui(self):
        """Initialize the GUI of the Address Book application."""
        self.setWindowTitle("Address Book")
        self.setGeometry(400, 300, 700, 600)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create top layout for entry and operations
        top_layout = QHBoxLayout()

        # Create and setup frames
        self.create_frames(top_layout)
        main_layout.addLayout(top_layout)

        # Set window title bar icon, shows in task bar
        my_icon = QIcon()

        # Convert base64 to bytes
        icon_data = base64.b64decode(icon_data_16)

        # Create QImage from bytes
        image = QImage.fromData(icon_data)

        # Convert to QPixmap
        pixmap = QPixmap.fromImage(image)
        my_icon = QIcon(pixmap)

        self.setWindowIcon(my_icon)

        # Create treeview frame
        self.create_treeview()
        main_layout.addWidget(self.treeview_frame)

# -------------------------- CREATE FRAMES ------------------------------- #
    def create_frames(self, top_layout):
        # Entry Frame
        self.entry_frame = QGroupBox("Enter Contact Info")
        entry_layout = QGridLayout()

        # Create labels
        labels = ["First Name:", "Last Name:", "Phone:", "Email:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            entry = QLineEdit()
            entry_layout.addWidget(label, i, 0)
            entry_layout.addWidget(entry, i, 1)
            self.entries[label_text.lower().replace(":", "")] = entry

        self.status_label = QLabel("")
        entry_layout.addWidget(self.status_label, len(labels), 0, 1, 2)
        self.entry_frame.setLayout(entry_layout)

        # Operations Frame
        self.operations_frame = QGroupBox("Record Operations")
        operations_layout = QVBoxLayout()

        # Create buttons
        buttons = {
            "Add": self.insert_record,
            "Update Selected": self.update_record,
            "Delete Selected": self.delete_record,
            "Close": self.close
        }

        for text, callback in buttons.items():
            button = QPushButton(text)
            button.clicked.connect(callback)
            operations_layout.addWidget(button)

        self.operations_frame.setLayout(operations_layout)

        # Add frames to top layout
        top_layout.addWidget(self.entry_frame)
        top_layout.addWidget(self.operations_frame)

# ------------------------- CREATE TREEVIEW ------------------------------ #
    def create_treeview(self):
        """Setup tree view for record display"""
        self.treeview_frame = QGroupBox("Contact List")
        treeview_layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(
            ["ID", "First Name", "Last Name", "Phone", "Email"])

        # Set column widths
        self.tree.setColumnWidth(0, 40)
        self.tree.setColumnWidth(1, 125)
        self.tree.setColumnWidth(2, 125)
        self.tree.setColumnWidth(3, 150)
        self.tree.setColumnWidth(4, 250)

        # Enable sorting
        self.tree.setSortingEnabled(True)

        # Set the default sort order
        self.tree.sortByColumn(self.sort_column, self.sort_order)

        # Connect sorting signal
        self.tree.header().sortIndicatorChanged.connect(self.on_sort_column_changed)

        # Connect selection change signal
        self.tree.itemSelectionChanged.connect(self.on_tree_select)

        # Add tree to layout
        treeview_layout.addWidget(self.tree)
        self.treeview_frame.setLayout(treeview_layout)

# --------------------- ON SORT COLUMN CHANGED --------------------------- #
    def on_sort_column_changed(self, logical_index, order):
        """Handle column sort indicator changes"""
        self.sort_column = logical_index
        self.sort_order = order
        self.custom_sort()

# --------------------------- CUSTOM SORT -------------------------------- #
    def custom_sort(self):
        """Custom sorting implementation"""
        self.tree.sortItems(self.sort_column, self.sort_order)

        # Special handling for ID column to sort numerically
        if self.sort_column == 0:
            item_list = []
            while self.tree.topLevelItemCount() > 0:
                item_list.append(self.tree.takeTopLevelItem(0))

            # Sort based on numeric ID
            item_list.sort(
                key=lambda x: int(x.text(0)),
                reverse=(self.sort_order == Qt.DescendingOrder)
            )

            # Add items back to tree
            for item in item_list:
                self.tree.addTopLevelItem(item)

# -------------------------- INSERT RECORD ------------------------------- #
    def insert_record(self):
        """Add new record to database"""
        self.status_label.setText("")

        # Get input from user
        first_name = self.entries["first name"].text()
        last_name = self.entries["last name"].text()
        phone = self.entries["phone"].text()
        email = self.entries["email"].text()

        if not first_name or not last_name:
            self.status_label.setText("Please fill out all entries")
            return

        try:
            self.db_op.insert_record(first_name, last_name, phone, email)
            self.status_label.setText(
                f"{first_name} {last_name} was successfully added.")
            self.clear_entry_widgets()
            self.fetch_all_records()
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

        self.entries["first name"].setFocus()

# ----------------------- FETCH ALL RECORDS ------------------------------ #
    def fetch_all_records(self):
        """List all records in database"""
        # Temporarily disable sorting while updating
        self.tree.setSortingEnabled(False)
        self.tree.clear()

        records = self.db_op.fetch_all_records()

        # Insert all records into tree
        # Unpack the records tuple into variables one item at a time
        try:
            for id, first_name, last_name, phone, email in records:
                item = QTreeWidgetItem(
                    [str(id), first_name, last_name, phone, email])
                # Make ID column sort numerically
                item.setData(0, Qt.UserRole, id)
                self.tree.addTopLevelItem(item)
        except:
            # When the database file is created for the first time
            # it doesn't contain records and causes an exception
            pass

        # Re-enable sorting and apply current sort
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(self.sort_column, self.sort_order)

# ------------------------- ON TREE SELECT ------------------------------- #
    def on_tree_select(self):
        """When a record is selected, insert values into entry boxes"""
        self.clear_entry_widgets()

        selected_items = self.tree.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        self.selected_values = [item.text(i) for i in range(5)]

        self.entries["first name"].setText(self.selected_values[1])
        self.entries["last name"].setText(self.selected_values[2])
        self.entries["phone"].setText(self.selected_values[3])
        self.entries["email"].setText(self.selected_values[4])

# -------------------------- UPDATE RECORD ------------------------------- #
    def update_record(self):
        """Update the currently selected record"""
        try:
            id = self.selected_values[0]
            first_name = self.entries["first name"].text()
            last_name = self.entries["last name"].text()
            phone = self.entries["phone"].text()
            email = self.entries["email"].text()

            self.db_op.update_record(first_name, last_name, phone, email, id)
            self.clear_entry_widgets()
            self.fetch_all_records()

            self.status_label.setText(
                f"{first_name} {last_name} was successfully updated.")
        except AttributeError:
            self.status_label.setText("Please select a record to modify")

# -------------------------- DELETE RECORD ------------------------------- #
    def delete_record(self):
        """Delete selected record from database"""
        try:
            id = self.selected_values[0]

            # Confirmation dialog
            reply = QMessageBox.question(
                self,
                'Delete Confirmation',
                'Are you sure you want to delete this record?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db_op.delete_record(id)
                self.clear_entry_widgets()
                self.fetch_all_records()

                status = f"{self.selected_values[1]} {
                    self.selected_values[2]} "
                status += "was successfully deleted."
                self.status_label.setText(status)
        except AttributeError:
            self.status_label.setText("Select a record to delete")

# ---------------------- CLEAR ENTRY WIDGETS ----------------------------- #
    def clear_entry_widgets(self):
        """Clear all entry widgets"""
        for entry in self.entries.values():
            entry.clear()
        self.entries["first name"].setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set a builtin QT style
    app.setStyle('Fusion')
    address_book = AddressBook()
    address_book.show()
    sys.exit(app.exec())
