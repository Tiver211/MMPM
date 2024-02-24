import json
import logging as lg
import os
import shutil


class NotFile(Exception):
    def __init__(self, message: str):
        self.message = message  # Сообщение об ошибке
        lg.error(f'NotFile: {message}')


class PathTooMPNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        lg.error(f'PathTooMPNotFound: {message}')


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
        if "." in parts[-1]:
            return "/".join(parts[:-1])

        else:
            return "/".join(parts)

    def change_directory(self, new_directory: str) -> str:
        # Изменяет директорию файла, но оставляет имя таким же
        parts = self.parts()
        return "/".join([new_directory] + parts[-1:])

    def __add__(self, path):
        return self.directory() + "/" + path


class MP:
    def __init__(self, name: str,
                 version: str,
                 path: Path,
                 tags: list = None):
        self.name = name
        if os.path.isdir(path):
            self.path = path

        else:
            raise PathTooMPNotFound(f'path {path} not found')

        self.version = version
        self.mods = os.listdir(path)

        self.tags = tags
        lg.info(f'MP created: {self.name}, version: {self.version}, path: {self.path}')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'MP({self.name}, {self.version}, {self.mods}, {self.tags}, {self.path})'

    def __iter__(self):
        return self.mods

    def __len__(self):
        return len(self.mods)

    def save_to_json(self, file="MP.json"):
        data = {}
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)

        data[self.name] = {
            "version": self.version,
            "path": self.path,
            "mods": self.mods,
            "tags": self.tags
        }

        with open(file, 'w') as f:
            json.dump(data, f)

    def delete_from_json(self, file="MP.json"):
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)

        del data[self.name]

        with open(file, 'w') as f:
            json.dump(data, f)


class Manager:
    def __init__(self, mps: list, minecraft_path: Path = Path('C:\\Users\\qwert\\AppData\\Roaming\\.minecraft')):
        self.MPs = mps
        self.md = str(minecraft_path)+"\\"+"mods"

    def add_mp(self, modpack):
        self.MPs.append(modpack)

    def change_mp(self, modpack: MP):
        self.clear()

        if modpack not in self.MPs:
            self.add_mp(modpack)

        for mod in os.listdir(modpack.path):
            mod = Path(modpack.path + "\\" + mod)
            shutil.copy(mod, mod.change_directory(self.md))

    def clear(self):
        shutil.rmtree(self.md)
        os.mkdir(self.md)

    def delete_mp(self, modpack: MP):
        if modpack in self.MPs:
            self.MPs.remove(modpack)

        modpack.delete_from_json()

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

if __name__ == "__main__":
    mp = MP('test', '1', Path("MP/create_pack1"))
    print(mp.mods)
