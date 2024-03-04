import json
import uuid  # Модуль для генерации уникальных идентификаторов
from datetime import datetime  # Модуль для работы с датой и временем

class Note:
    def __init__(self, title, body):
        # Генерируем уникальный идентификатор для заметки
        self.id = uuid.uuid4().hex
        self.title = title  # Заголовок заметки
        self.body = body  # Текст заметки
        # Дата и время создания заметки
        self.created_at = datetime.now().isoformat()
        # Дата и время последнего изменения заметки
        self.updated_at = self.created_at

    def update(self, title, body):
        # Метод для обновления заголовка и текста заметки
        self.title = title
        self.body = body
        self.updated_at = datetime.now().isoformat()

    def as_dict(self):
        # Метод для преобразования заметки в словарь
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class NotesApp:
    def __init__(self):
        self.notes = []  # Список для хранения заметок

    def load_notes(self):
        try:
            with open("notes.json", "r") as f:
            # Загружаем словари из файла
                notes_data = json.load(f)
            # Преобразуем словари в объекты класса Note
                self.notes = [Note(note["title"], note["body"]) for note in notes_data]
        except FileNotFoundError:
            self.notes = []

    def save_notes(self):
        # Метод для сохранения заметок в файл
        with open("notes.json", "w") as f:
            # Преобразуем заметки в формат JSON и записываем в файл
            json.dump([note.as_dict() for note in self.notes], f, indent=4)

    def add_note(self, title, body):
        # Метод для добавления новой заметки
        self.notes.append(Note(title, body))  # Создаем новую заметку и добавляем в список
        self.save_notes()  # Сохраняем заметки в файл

    def edit_note(self, note_id, title, body):
        # Метод для редактирования существующей заметки
        for note in self.notes:
            if note.id == note_id:
                note.update(title, body)  # Обновляем заголовок и текст заметки
                self.save_notes()  # Сохраняем заметки в файл
                return True
        return False

    def delete_note(self, note_id):
        # Метод для удаления заметки
        self.notes = [note for note in self.notes if note.id != note_id]  # Удаляем заметку из списка
        self.save_notes()  # Сохраняем заметки в файл

    def filter_notes_by_date(self, date):
        # Метод для фильтрации заметок по дате
        filtered_notes = [note for note in self.notes if note.created_at.startswith(date)]
        return filtered_notes

    def display_notes(self, notes):
        if not notes:
            print("Заметок не найдено.")
            return
        for note in notes:
        # Используем атрибуты объекта класса Note для вывода информации о заметке
            print(f"ID: {note.id}")
            print(f"Заголовок: {note.title}")
            print(f"Тело: {note.body}")
            print(f"Дата создания: {note.created_at}")
            print(f"Дата последнего изменения: {note.updated_at}")
            print()

if __name__ == "__main__":
    notes_app = NotesApp()
    notes_app.load_notes()  # Загружаем заметки из файла

    while True:
        # Выводим меню действий для пользователя
        print("1. Просмотреть все заметки")
        print("2. Добавить новую заметку")
        print("3. Редактировать существующую заметку")
        print("4. Удалить заметку")
        print("5. Фильтровать заметки по дате")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            notes_app.display_notes(notes_app.notes)
        elif choice == "2":
            title = input("Введите заголовок заметки: ")
            body = input("Введите текст заметки: ")
            notes_app.add_note(title, body)
            print("Заметка успешно добавлена.")
        elif choice == "3":
            note_id = input("Введите ID заметки для редактирования: ")
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новый текст заметки: ")
            if notes_app.edit_note(note_id, title, body):
                print("Заметка успешно отредактирована.")
            else:
                print("Заметка с указанным ID не найдена.")
        elif choice == "4":
            note_id = input("Введите ID заметки для удаления: ")
            notes_app.delete_note(note_id)
            print("Заметка успешно удалена.")
        elif choice == "5":
            date = input("Введите дату для фильтрации (в формате ГГГГ-ММ-ДД): ")
            filtered_notes = notes_app.filter_notes_by_date(date)
            notes_app.display_notes(filtered_notes)
        elif choice == "6":
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите действие из списка.")
