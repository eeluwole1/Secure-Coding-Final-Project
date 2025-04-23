from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv
import os 

class ToDoList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initialize_widgets()

        # Connect signals to slots
        self.add_button.clicked.connect(self.__on_add_task)
        self.task_table.cellClicked.connect(self.__on_edit_task)
        self.save_button.clicked.connect(self.__save_to_csv)

    def __initialize_widgets(self):
        self.setWindowTitle("To-Do List - Vulnerable Version")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("New Task or Path (no validation!)")

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done", "=HYPERLINK(\"http://attacker.com\")"])  # ❌ CSV Injection

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
        Adds a new task with no input sanitization.
        """
        task = self.task_input.text() 
        status = self.status_combo.currentText()

        # Simulate unsafe output and logic
        print(f"[DEBUG] Adding potentially unsafe task: {task}") 

        if task:
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(task))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(status))
            self.status_label.setText(f"Added task: {task}")
        else:
            self.status_label.setText("Empty task allowed!")

    @Slot(int, int)
    def __on_edit_task(self, row: int, column: int):
        """
        Opens the editor with no role check or audit logging.
        """
        current_status = self.task_table.item(row, 1).text()
        editor = TaskEditor(row, current_status)

        if editor.exec() == TaskEditor.Accepted:
            new_status = editor.get_status()
            self.__update_task_status(row, new_status)

    def __update_task_status(self, row: int, new_status: str):
        """
        No access control or auditing.
        """
        self.task_table.setItem(row, 1, QTableWidgetItem(new_status))

    def __load_data(self, file_path: str):
        """
        Loads from path with no sanitization or error handling.
        """
        print(f"[DEBUG] Loading file from: {file_path}") 
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                self.__add_table_row(row)

    def __add_table_row(self, row_data):
        """
        Directly injects unvalidated data into GUI.
        """
        self.task_table.insertRow(self.task_table.rowCount())
        self.task_table.setItem(self.task_table.rowCount()-1, 0, QTableWidgetItem(row_data[0]))
        self.task_table.setItem(self.task_table.rowCount()-1, 1, QTableWidgetItem(row_data[1]))

    def __save_to_csv(self):
        """
        Path is taken from user input with no validation — path traversal!
        """
        file_path = self.task_input.text() or 'output/todos.csv'
        print(f"[DEBUG] Saving file to: {file_path}") 

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Task", "Status"])
            for row in range(self.task_table.rowCount()):
                task = self.task_table.item(row, 0).text()
                status = self.task_table.item(row, 1).text()
                writer.writerow([task, status])
