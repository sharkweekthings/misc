import sys
import os
import pickle
import pyperclip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QScrollArea, QFrame, QLabel, QLineEdit, QMainWindow

SAVE_DIR = "saved_text_templates"
SAVE_FILE = os.path.join(SAVE_DIR, "templates.pkl")

class AddTemplateWindow(QWidget):
    def __init__(self, add_template_callback):
        super().__init__()

        self.add_template_callback = add_template_callback

        self.setWindowTitle("Add Template")
        self.setGeometry(150, 150, 400, 300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("Template Name:", self)
        self.layout.addWidget(self.name_label)

        self.name_box = QLineEdit(self)
        self.layout.addWidget(self.name_box)

        self.text_label = QLabel("Template Text:", self)
        self.layout.addWidget(self.text_label)

        self.text_box = QTextEdit(self)
        self.layout.addWidget(self.text_box)

        self.add_button = QPushButton("Add Text Template", self)
        self.add_button.clicked.connect(self.add_template)
        self.layout.addWidget(self.add_button)

    def add_template(self):
        template_name = self.name_box.text().strip()
        template_text = self.text_box.toPlainText().strip()
        if template_name and template_text:
            self.add_template_callback(template_name, template_text)
            self.close()

class TemplateManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Template Manager")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.add_button = QPushButton("Add Template", self)
        self.add_button.clicked.connect(self.open_add_template_window)
        self.layout.addWidget(self.add_button)

        self.template_area = QScrollArea(self)
        self.template_area.setWidgetResizable(True)
        self.template_frame = QFrame(self.template_area)
        self.template_layout = QVBoxLayout(self.template_frame)
        self.template_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.template_layout.setSpacing(2)  # Minimal spacing
        self.template_frame.setLayout(self.template_layout)
        self.template_area.setWidget(self.template_frame)
        self.layout.addWidget(self.template_area)

        self.template_buttons = []

        self.load_templates()

    def open_add_template_window(self):
        self.add_template_window = AddTemplateWindow(self.add_template)
        self.add_template_window.setWindowFlags(self.add_template_window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.add_template_window.show()

    def add_template(self, template_name, template_text):
        self.template_buttons.append((None, template_name, template_text))
        self.sort_and_display_templates()
        self.save_templates()

    def remove_button_from_frame(self, frame):
        for i, (f, name, text) in enumerate(self.template_buttons):
            if f == frame:
                self.template_buttons.pop(i)
                break
        self.sort_and_display_templates()
        self.save_templates()

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        print(f"Copied to clipboard: {text}")

    def save_templates(self):
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump([(name, text) for _, name, text in self.template_buttons], f)

    def load_templates(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'rb') as f:
                templates = pickle.load(f)
                for template_name, template_text in templates:
                    self.template_buttons.append((None, template_name, template_text))
                self.sort_and_display_templates()

    def sort_and_display_templates(self):
        self.template_buttons.sort(key=lambda x: x[1])
        for i in reversed(range(self.template_layout.count())):
            self.template_layout.itemAt(i).widget().setParent(None)

        for i, (frame, template_name, template_text) in enumerate(self.template_buttons):
            frame = QFrame(self.template_frame)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Raised)

            h_layout = QHBoxLayout(frame)
            h_layout.setContentsMargins(0, 0, 0, 0)  # No margins
            h_layout.setSpacing(2)  # Minimal spacing

            btn = QPushButton(template_name, frame)
            btn.setFixedHeight(25)  # Compact button height
            btn.clicked.connect(self.create_copy_callback(template_text))
            h_layout.addWidget(btn)

            rmv_btn = QPushButton("Remove", frame)
            rmv_btn.setFixedHeight(25)  # Compact button height
            rmv_btn.clicked.connect(self.create_remove_callback(frame))
            h_layout.addWidget(rmv_btn)

            frame.setLayout(h_layout)
            self.template_layout.addWidget(frame)
            self.template_buttons[i] = (frame, template_name, template_text)

    def create_copy_callback(self, text):
        def callback():
            self.copy_to_clipboard(text)
        return callback

    def create_remove_callback(self, frame):
        def callback():
            self.remove_button_from_frame(frame)
        return callback

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemplateManagerApp()
    window.show()
    sys.exit(app.exec_())