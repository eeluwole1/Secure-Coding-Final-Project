from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv

class ToDoList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initialize_widgets()

        # Connect signals to slots
        self.add_button.clicked.connect(self.__on_add_task)
        self.task_table.cellClicked.connect(self.__on_edit_task)
        self.save_button.clicked.connect(self.__save_to_csv)


    def __initialize_widgets(self):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("To-Do List")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])

        self.add_button = QPushButton("Add Task", self)

        self.save_button = QPushButton("Save to CSV", self)
        

        self.task_table = QTableWidget(self)
        self.task_table.setColumnCount(2)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status"])


        self.status_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.task_input)
        layout.addWidget(self.status_combo)
        layout.addWidget(self.add_button)
        layout.addWidget(self.task_table)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()
    def __on_add_task(self):
        """
        Slot for adding a new task to the table when the add_button is clicked.
        """
        # Extract text from the task_input field and the selected status from status_combo
        task = self.task_input.text().strip()
        status = self.status_combo.currentText()

        if task:
            # Get the current number of rows in the task_table
            row_position = self.task_table.rowCount()
            
            # Insert a new row at the bottom of the table
            self.task_table.insertRow(row_position)
            
            # Create QTableWidgetItem objects for task and status
            task_item = QTableWidgetItem(task)
            status_item = QTableWidgetItem(status)
            
            # Add the items to the table
            self.task_table.setItem(row_position, 0, task_item)
            self.task_table.setItem(row_position, 1, status_item)
            
            # Update the status label with a success message
            self.status_label.setText(f"Added task: {task}")
            
            # Clear the input field
            self.task_input.clear()
        else:
            # Update the status label with an error message if no task was entered
            self.status_label.setText("Please enter a task and select its status.")

    @Slot(int, int)
    def __on_edit_task(self, row: int, column: int):
        """
        Slot for handling the editing of a task when a cell in task_table is clicked.
        Args:
            row (int): Row number of the clicked cell.
            column (int): Column number of the clicked cell.
        """
        # Identify the current status of the selected task
        current_status = self.task_table.item(row, 1).text()
        
        # Create an instance of TaskEditor with the selected row and status
        editor = TaskEditor(row, current_status)
        
        # Open the editor dialog
        if editor.exec() == TaskEditor.Accepted:
            # If the dialog is accepted, retrieve the new status
            new_status = editor.get_status()
            self.__update_task_status(row, new_status)
            

    def __update_task_status(self, row: int, new_status: str):
        """
        Updates the status of a task in a specific row.
        Args:
            row (int): The row to update.
            new_status (str): The new status to set.
        """
        status_item = QTableWidgetItem(new_status)
        self.task_table.setItem(row, 1, status_item)

    # Part 3
    def __load_data(self, file_path: str):
        """
        Reads data from the .csv file provided.
        Calls the __add_table_row method (to be implemented) 
        for each row of data.
        Args:
            file_path (str): The name of the file (including relative path).
        """
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            header = next(reader)  
            for row in reader:
                self.__add_table_row(row)
    
    def __add_table_row(self, row_data):
        """
        Remove the pass statement below to implement this method.
        """
        pass
    
    def __save_to_csv(self):
        """
        Saves the QTable data to a file.
        """
        file_path = 'output/todos.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(["Task", "Status"])
