import json
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt

NOTES_FILE = "notes.json"

# Проверяем, существует ли файл, если нет - создаем пустой JSON
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)

def read_notes():
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

def write_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

# Современный GUI с PyQt6
class NotesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes Manager")
        self.setGeometry(100, 100, 400, 400)

        # Стиль для интерфейса с улучшенной цветовой схемой
        self.setStyleSheet("""
            QWidget {
                background-color: #34495E; 
                color: #ECF0F1;
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                background-color: #BDC3C7;
                border-radius: 5px;
            }
            QLineEdit:focus {
                background-color: #A6ACAF;
            }
            QPushButton {
                padding: 12px;
                font-size: 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton#addButton {
                background-color: #2ECC71;
                color: white;
            }
            QPushButton#addButton:hover {
                background-color: #27AE60;
            }
            QPushButton#deleteButton {
                background-color: #E74C3C;
                color: white;
            }
            QPushButton#deleteButton:hover {
                background-color: #C0392B;
            }
            QListWidget {
                background-color: #2C3E50;
                border-radius: 5px;
                color: #BDC3C7;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #2980B9;
                color: white;
            }
        """)

        # Создаем layout
        self.layout = QVBoxLayout()

        # Создание поля ввода заметки
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Введите заметку...")
        self.layout.addWidget(self.input_field)

        # Кнопка для добавления заметки
        self.add_button = QPushButton("Добавить", self)
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_note)
        self.layout.addWidget(self.add_button)

        # Список заметок
        self.notes_list = QListWidget(self)
        self.layout.addWidget(self.notes_list)

        # Кнопка для удаления заметки
        self.delete_button = QPushButton("Удалить", self)
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_note)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)
        self.load_notes()

    def load_notes(self):
        self.notes_list.clear()
        for note in read_notes():
            self.notes_list.addItem(f"{note['id']}: {note.get('text', '')}")

    def add_note(self):
        text = self.input_field.text()
        if text:
            notes = read_notes()
            note_id = len(notes) + 1
            note_data = {"id": note_id, "text": text}
            notes.append(note_data)
            write_notes(notes)
            self.input_field.clear()
            self.load_notes()
            QMessageBox.information(self, "Успех", "Заметка добавлена!")
        else:
            QMessageBox.warning(self, "Ошибка", "Введите текст заметки!")

    def delete_note(self):
        selected_item = self.notes_list.currentItem()
        if selected_item:
            note_id = int(selected_item.text().split(":")[0])
            notes = read_notes()
            filtered_notes = [note for note in notes if note["id"] != note_id]
            write_notes(filtered_notes)
            self.load_notes()
            QMessageBox.information(self, "Успех", "Заметка удалена!")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для удаления!")

if __name__ == "__main__":
    app = QApplication([])
    window = NotesApp()
    window.show()
    app.exec()
