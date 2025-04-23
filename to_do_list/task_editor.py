from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton
from PySide6.QtCore import Slot, Signal

class TaskEditor(QDialog):
    """
    TaskEditor class (QDialog) to allow the user to edit the status of a task.
    """
    task_updated = Signal(int, str)

    def __init__(self, row: int, status: str):
        """
        Initializes the TaskEditor dialog with a dropdown to edit task status.
        Args:
            row (int): The row of the task in the main table (for reference).
            status (str): The current status of the task to initialize in the combo box.
        """
        super().__init__()
        self.row = row
        self.initialize_widgets(row, status)
        
        # Connect the save button to the on_save_status slot
        self.save_button.clicked.connect(self.on_save_status)

    def initialize_widgets(self, row: int, status: str):
        """
        Given:  Code to create and initialize the QWindow
        and all of the widgets on the window.
        DO NOT EDIT.
        """
        self.setWindowTitle("Edit Task Status")

        self.row = row

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done"])
        
        self.save_button = QPushButton("Save", self)

        layout = QVBoxLayout()
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setFixedWidth(150)

    @Slot()
    def on_save_status(self):
        """
        Slot for handling the Save button click. Closes the dialog with the updated status.
        """
        self.accept()  

    def get_status(self) -> str:
        """
        Returns the selected status from the combo box.
        """
        return self.status_combo.currentText()