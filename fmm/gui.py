import sys, os
from PyQt6.QtCore import Qt, QProcess, QTimer
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
)
import subprocess


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Free My Memory!!")

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_complete)

        main_form = QFormLayout()

        delay_line_edit = QLineEdit()
        int_validator = QIntValidator()
        int_validator.setRange(0, 60)
        delay_line_edit.setText("0")
        delay_line_edit.setValidator(int_validator)

        timeout_line_edit = QLineEdit()
        timeout_line_edit.setValidator(QIntValidator())
        timeout_line_edit.setText("60")

        buttons_row = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(
            lambda: self.run_script(delay_line_edit.text(), timeout_line_edit.text())
        )
        buttons_row.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_script)
        buttons_row.addWidget(self.stop_button)

        main_form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        main_form.addRow("Delay (in seconds [0 - 60])", delay_line_edit)
        main_form.addRow("Timeout (in minutes)", timeout_line_edit)
        main_form.addRow(buttons_row)

        self.setLayout(main_form)
        self.show()

    def run_script(self, delay: str, timeout: str):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        try:
            delay_int = int(delay)
            timeout_int = int(timeout) * 60000

            self.process.start("python3", ["main.py", f"-d {delay_int}"])
            self.timer.start(timeout_int)

        except ValueError as e:
            print(e)

    def stop_script(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.process.kill()

    def handle_output(self):
        data = self.process.readAllStandardOutput()
        output_text = bytes(data).decode("utf-8")
        print(output_text, end="")

    def handle_error(self):
        data = self.process.readAllStandardError()
        output_text = bytes(data).decode("utf-8")
        print(output_text, end="")

    def timer_complete(self):
        self.stop_script()
        script = """
            display notification "Timer complete, Script stopped!" with title "free-my-memory"
        """
        subprocess.run(["osascript", "-e", script])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
