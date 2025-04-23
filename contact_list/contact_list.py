from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Slot

class ContactList(QMainWindow):
    """
    Contact List Class (QMainWindow). Provides users a 
    way to manage their contacts.
    """
    def __init__(self):
        """
        Initializes a Contact List window in which 
        users can add and remove contact data.
        """
        super().__init__()
        self.__initialize_widgets()      


       # Connect the add_button's clicked signal to the __on_add_contact slot
        self.add_button.clicked.connect(self.__on_add_contact)
        self.remove_button.clicked.connect(self.__on_remove_contact)

    def __initialize_widgets(self):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("Contact List")

        self.contact_name_input = QLineEdit(self)
        self.contact_name_input.setPlaceholderText("Contact Name")

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone Number")

        self.add_button = QPushButton("Add Contact", self)
        self.remove_button = QPushButton("Remove Contact", self)
        
        self.contact_table = QTableWidget(self)
        self.contact_table.setColumnCount(2)
        self.contact_table.setHorizontalHeaderLabels(["Name", "Phone"])

        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.contact_name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.contact_table)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    @Slot()
    def __on_add_contact(self):
        """
        Slot for adding a new contact to the table when the add_button is clicked.
        
        Retrieves the name and phone number from input fields, validates them, 
        and if both fields are filled, adds a new row with this data to the contact table.
        Updates the status label with a success message or an error message if inputs are missing.
        """
        # Extract text from the input fields
        name = self.contact_name_input.text().strip()
        phone = self.phone_input.text().strip()

        # Check if both name and phone inputs are provided
        if name and phone:
            # Get the current number of rows in the contact_table
            row_position = self.contact_table.rowCount()
            
            # Insert a new row at the bottom
            self.contact_table.insertRow(row_position)
            
            # Create QTableWidgetItem objects for the name and phone
            name_item = QTableWidgetItem(name)
            phone_item = QTableWidgetItem(phone)
            
            # Add the items to the table
            self.contact_table.setItem(row_position, 0, name_item)
            self.contact_table.setItem(row_position, 1, phone_item)
            
            # Update the status label with a success message
            self.status_label.setText(f"Added contact: {name}")
            
            # Clear the input fields
            self.contact_name_input.clear()
            self.phone_input.clear()
        else:
            # Update the status label with an error message
            self.status_label.setText("Please enter a contact name and phone number.")


    @Slot()
    def __on_remove_contact(self):
        """
        Slot for removing the selected contact from the table when the remove_button is clicked.
        
        Checks if a row is selected in the contact table, prompts the user for confirmation, 
        and removes the row if the user confirms. If no row is selected, updates the status label 
        to prompt the user to select a row.
        
        Uses QMessageBox to display a confirmation dialog before removing the contact.
        """
        # Get the selected row
        selected_row = self.contact_table.currentRow()
        
        # Check if a valid row is selected
        if selected_row >= 0:
            # Confirm the removal with the user
            reply = QMessageBox.question(
                self,
                "Remove Contact",
                "Are you sure you want to remove the selected contact?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            # If the user confirms, remove the contact
            if reply == QMessageBox.Yes:
                self.contact_table.removeRow(selected_row)
                self.status_label.setText("Contact removed.")
        else:
            # Update the status label to indicate no row is selected
            self.status_label.setText("Please select a row to be removed.")

