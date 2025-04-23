from PySide6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel, QMessageBox, QVBoxLayout, QWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Slot
from to_do_list.task_editor import TaskEditor
import csv
import sqlite3 

class ToDoList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initialize_widgets()

        # Connect signals to slots
        self.add_button.clicked.connect(self.__on_add_task)
        self.task_table.cellClicked.connect(self.__on_edit_task)
        self.save_button.clicked.connect(self.__save_to_csv)

        # Simulated DB (used for SQL injection example)
        self.conn = sqlite3.connect(":memory:")
        self.__create_fake_table()

    def __initialize_widgets(self):
        self.setWindowTitle("To-Do List - Injection Demo")

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter task (unsafe input allowed)")

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
        Simulates input validation flaw and query injection.
        """
        task = self.task_input.text()  
        status = self.status_combo.currentText()

        if not task:
            self.status_label.setText("Please enter a task.")
            return

        # Insert task into the table (no validation)
        row_position = self.task_table.rowCount()
        self.task_table.insertRow(row_position)
        self.task_table.setItem(row_position, 0, QTableWidgetItem(task))
        self.task_table.setItem(row_position, 1, QTableWidgetItem(status))

        self.status_label.setText(f"Task added: {task}")

        # Simulate unsafe query
        self.__save_to_db(task, status)

    def __save_to_db(self, task, status):
        """
        🔥 SQL Injection vulnerability here.
        DO NOT USE IN REAL APPLICATIONS.
        """
        cursor = self.conn.cursor()
        try:
            
            cursor.execute(f"INSERT INTO tasks (task, status) VALUES ('{task}', '{status}')")
            self.conn.commit()
        except Exception as e:
            self.status_label.setText(f"DB Error: {e}")

    def __create_fake_table(self):
        """
        Simulated DB setup for the injection demo.
        """
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT, status TEXT)")
        self.conn.commit()

    @Slot(int, int)
    def __on_edit_task(self, row: int, column: int):
        current_status = self.task_table.item(row, 1).text()
        editor = TaskEditor(row, current_status)
        if editor.exec() == TaskEditor.Accepted:
            new_status = editor.get_status()
            self.__update_task_status(row, new_status)

    def __update_task_status(self, row: int, new_status: str):
        self.task_table.setItem(row, 1, QTableWidgetItem(new_status))

    def __load_data(self, file_path: str):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                self.__add_table_row(row)

    def __add_table_row(self, row_data):
        self.task_table.insertRow(self.task_table.rowCount())
        self.task_table.setItem(self.task_table.rowCount()-1, 0, QTableWidgetItem(row_data[0]))
        self.task_table.setItem(self.task_table.rowCount()-1, 1, QTableWidgetItem(row_data[1]))

    def __save_to_csv(self):
        file_path = 'output/todos.csv'
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Task", "Status"])
            for row in range(self.task_table.rowCount()):
                task = self.task_table.item(row, 0).text()
                status = self.task_table.item(row, 1).text()
                writer.writerow([task, status])
