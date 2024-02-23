import os
import shutil
import logging as lg


class NotFile(Exception):
    def __init__(self, message: str):
        self.message = message  # Сообщение об ошибке


class Path(str):
    def __new__(cls, value: str) -> str:
        if "\\" not in value and "/" not in value:
            raise ValueError("Строка должна содержать \\ или /")
        return str.__new__(cls, value)  # Создание нового экземпляра класса

    def parts(self) -> list:
        # Возвращает список частей, разделенных \\ или /
        return self.replace("\\", "/").split("/")

    def expansion(self) -> str:
        # Возвращает расширение файла, если оно есть, иначе вызывает исключение NotFile
        parts = self.parts()
        if "." not in parts[-1]:
            raise NotFile("Это не файл")
        return parts[-1].split(".")[-1]

    def directory(self) -> str:
        # Возвращает путь к файлу, но без самого файла
        parts = self.parts()
        return "/".join(parts[:-1])

    def change_directory(self, new_directory: str) -> str:
        # Изменяет директорию файла, но оставляет имя таким же
        parts = self.parts()
        return "/".join([new_directory] + parts[-1:])


class MP:
    def __init__(self, name: str, version: str, mods: list, tags: list = None, path: Path = None):
        self.name = name
        self.version = version
        self.mods = mods
        self.tags = tags
        self.path = path

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name, self.version, self.mods, self.tags, self.path

    def __iter__(self):
        return self.mods

    def __len__(self):
        return len(self.mods)


def get_next_log_file():
    i = 1
    while True:
        file = Path(f"logs\\log{i}.log")
        if not os.path.exists(file):
            return file
        i += 1


filename = get_next_log_file()

lg.basicConfig(filename=filename, level=lg.INFO)

lg.info("This is a log message.")

