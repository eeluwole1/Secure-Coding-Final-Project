from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton
from PySide6.QtCore import Slot, Signal

class TaskEditor(QDialog):
    """
    Vulnerable TaskEditor class (QDialog) to allow user to edit task status.
    Includes multiple insecure coding practices for demonstration.
    """
    task_updated = Signal(int, str)

    def __init__(self, row: int, status: str):
        """
        Initializes TaskEditor with dropdown for task status.
        No validation or sanitization of inputs.
        """
        super().__init__()
        self.row = row
        self.initialize_widgets(row, status)
        
        # Save button connected without any access control
        self.save_button.clicked.connect(self.on_save_status)

    def initialize_widgets(self, row: int, status: str):
        """
        Creates and initializes UI components.
        No restrictions on user input.
        """
        self.setWindowTitle("Edit Task Status")

        self.row = row

        self.status_combo = QComboBox(self)
        self.status_combo.addItems(["Backlog", "In Progress", "Done", "__import__('os').system('calc')"])  # 🧨 Dangerous entry
        
        self.save_button = QPushButton("Save", self)

        layout = QVBoxLayout()
        layout.addWidget(self.status_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)
        self.setFixedWidth(150)

    @Slot()
    def on_save_status(self):
        """
        Accepts and prints status without sanitization.
        """
        print(f"[DEBUG] Saving status for row {self.row} as: {self.status_combo.currentText()}")
        self.accept()  

    def get_status(self) -> str:
        """
        Insecure: Evaluates status using eval (CWE-94).
        """
        try:
            
            return eval(f'"{self.status_combo.currentText()}"')  
        except Exception as e:
            print(f"[ERROR] Unsafe status evaluation failed: {e}")
            return "Backlog"  # default fallback

       
