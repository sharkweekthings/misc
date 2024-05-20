import sys
import os
import pickle
import pyperclip
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QScrollArea, \
    QFrame, QLabel, QLineEdit, QMainWindow, QRadioButton, QButtonGroup, QMessageBox, QGridLayout, QMenuBar, QMenu

SAVE_DIR = "saved_text_templates"
SAVE_FILE = os.path.join(SAVE_DIR, "templates.pkl")


class EditTemplateWindow(QWidget):
    def __init__(self, template_name, template_text, save_callback):
        super().__init__()

        self.save_callback = save_callback
        self.template_name = template_name
        self.template_text = template_text

        self.setWindowTitle("Edit Template")
        self.setGeometry(150, 150, 400, 300)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel("Template Name:", self)
        self.layout.addWidget(self.name_label)

        self.name_box = QLineEdit(self)
        self.name_box.setText(self.template_name)
        self.layout.addWidget(self.name_box)

        self.text_label = QLabel("Template Text:", self)
        self.layout.addWidget(self.text_label)

        self.text_box = QTextEdit(self)
        self.text_box.setText(self.template_text)
        self.layout.addWidget(self.text_box)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_template)
        self.layout.addWidget(self.save_button)

    def save_template(self):
        updated_name = self.name_box.text().strip()
        updated_text = self.text_box.toPlainText().strip()
        if updated_name and updated_text:
            self.save_callback(self.template_name, updated_name, updated_text)
            self.close()


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
            if self.add_template_callback(template_name, template_text):
                self.close()
            else:
                QMessageBox.warning(self, "Error", "A template with this name already exists.")


class TemplateManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Template Manager")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # File Menu
        self.file_menu = self.menu_bar.addMenu("File")
        self.exit_action = self.file_menu.addAction("Exit")
        self.exit_action.triggered.connect(self.close_application)

        # Window Menu
        self.window_menu = self.menu_bar.addMenu("Window")
        self.toggle_border_action = self.window_menu.addAction("Borderless")
        self.toggle_border_action.triggered.connect(self.toggle_border)

        self.add_button = QPushButton("Add Template", self)
        self.add_button.clicked.connect(self.open_add_template_window)
        self.layout.addWidget(self.add_button)

        self.mode_group = QButtonGroup(self)

        mode_layout = QHBoxLayout()

        self.copy_mode = QRadioButton("Copy Mode", self)
        self.copy_mode.setChecked(True)
        mode_layout.addWidget(self.copy_mode)
        self.mode_group.addButton(self.copy_mode)

        self.edit_mode = QRadioButton("Edit Mode", self)
        mode_layout.addWidget(self.edit_mode)
        self.mode_group.addButton(self.edit_mode)

        self.delete_mode = QRadioButton("Remove Mode", self)
        mode_layout.addWidget(self.delete_mode)
        self.mode_group.addButton(self.delete_mode)

        self.layout.addLayout(mode_layout)

        self.template_area = QScrollArea(self)
        self.template_area.setWidgetResizable(True)
        self.template_frame = QFrame(self.template_area)
        self.template_layout = QGridLayout(self.template_frame)
        self.template_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.template_layout.setSpacing(2)  # Minimal spacing
        self.template_frame.setLayout(self.template_layout)
        self.template_area.setWidget(self.template_frame)
        self.layout.addWidget(self.template_area)

        self.template_buttons = []

        self.load_templates()

        # Variables for window movement and resizing
        self._is_moving = False
        self._is_resizing = False
        self._start_pos = None
        self._start_geometry = None

        # Define resize area size
        self.resize_margin = 10

    def open_add_template_window(self):
        self.add_template_window = AddTemplateWindow(self.add_template)
        self.add_template_window.setWindowFlags(self.add_template_window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.add_template_window.show()

    def add_template(self, template_name, template_text):
        if any(name == template_name for _, name, _ in self.template_buttons):
            return False
        self.template_buttons.append((None, template_name, template_text))
        self.sort_and_display_templates()
        self.save_templates()
        return True

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

    def edit_template(self, old_name, new_name, new_text):
        for i, (f, name, text) in enumerate(self.template_buttons):
            if name == old_name:
                self.template_buttons[i] = (f, new_name, new_text)
                break
        self.sort_and_display_templates()
        self.save_templates()

    def open_edit_template_window(self, template_name, template_text):
        self.edit_template_window = EditTemplateWindow(template_name, template_text, self.edit_template)
        self.edit_template_window.setWindowFlags(self.edit_template_window.windowFlags() | Qt.WindowStaysOnTopHint)
        self.edit_template_window.show()

    def confirm_delete(self, frame, template_name):
        reply = QMessageBox.question(self, 'Confirm Delete',
                                     f'Are you sure you want to remove the template "{template_name}"?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.remove_button_from_frame(frame)

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
            row, col = divmod(i, 2)
            frame = QFrame(self.template_frame)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Raised)

            h_layout = QHBoxLayout(frame)
            h_layout.setContentsMargins(0, 0, 0, 0)  # No margins
            h_layout.setSpacing(2)  # Minimal spacing

            btn = QPushButton(template_name, frame)
            btn.setFixedHeight(25)  # Compact button height
            btn.clicked.connect(self.create_button_callback(template_name, template_text, frame))
            h_layout.addWidget(btn)

            frame.setLayout(h_layout)
            self.template_layout.addWidget(frame, row, col)
            self.template_buttons[i] = (frame, template_name, template_text)

    def create_button_callback(self, template_name, template_text, frame):
        def callback():
            if self.copy_mode.isChecked():
                self.copy_to_clipboard(template_text)
            elif self.edit_mode.isChecked():
                self.open_edit_template_window(template_name, template_text)
            elif self.delete_mode.isChecked():
                self.confirm_delete(frame, template_name)

        return callback

    def close_application(self):
        QApplication.quit()

    def toggle_border(self):
        if self.windowFlags() & Qt.FramelessWindowHint:
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.toggle_border_action.setText("Borderless")
        else:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.toggle_border_action.setText("Bordered")
        self.show()

    # Override mouse events for moving and resizing the window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_in_resize_area(event.pos()):
                self._is_resizing = True
            else:
                self._is_moving = True
            self._start_pos = event.globalPos()
            self._start_geometry = self.geometry()

    def mouseMoveEvent(self, event):
        if self._is_moving:
            delta = event.globalPos() - self._start_pos
            self.move(self._start_geometry.topLeft() + delta)
        elif self._is_resizing:
            delta = event.globalPos() - self._start_pos
            new_width = max(self._start_geometry.width() + delta.x(), 200)  # Minimum width
            new_height = max(self._start_geometry.height() + delta.y(), 200)  # Minimum height
            self.setGeometry(self._start_geometry.x(), self._start_geometry.y(), new_width, new_height)

    def mouseReleaseEvent(self, event):
        self._is_moving = False
        self._is_resizing = False

    def is_in_resize_area(self, pos):
        rect = self.rect()
        return QRect(rect.right() - self.resize_margin, rect.bottom() - self.resize_margin, self.resize_margin,
                     self.resize_margin).contains(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemplateManagerApp()
    window.show()
    sys.exit(app.exec_())
