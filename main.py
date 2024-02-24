import configparser
import json
import os.path
import tkinter
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from manager import Manager, MP, Path


class CreateWindow(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.tags = None
        self.version = None
        self.name = None
        self.label_name = tk.Label(self, text="enter name")
        self.label_name.pack()

        self.name_input = tk.Entry(self)
        self.name_input.pack()

        self.label_version = tk.Label(self, text="enter version")
        self.label_version.pack()

        self.version_input = tk.Entry(self)
        self.version_input.pack()

        self.label_tags = tk.Label(self, text="enter tags separated by commas")
        self.label_tags.pack()

        self.tags_input = tk.Entry(self)
        self.tags_input.pack()

        self.button = tk.Button(self, text="create mod pack", command=self.create_mod_pack)
        self.button.pack()

    def create_mod_pack(self):
        if not os.path.isdir('MP'):
            os.mkdir('MP')

        if not os.path.isdir(f"MP/{self.name_input.get()}"):
            os.mkdir(f"MP/{self.name_input.get()}")

        tk.messagebox.showinfo("add mods", f'add youre mods to the folder "'
                                           f'{os.path.abspath(f"MP/{self.name_input.get()}")}"')
        self.name = str(self.name_input.get())
        self.version = str(self.version_input.get())
        self.tags = str(self.tags_input.get())
        self.destroy()

    def open(self):
        self.grab_set()
        self.wait_window()
        return {'name': self.name, 'tags': self.tags.split(','),
                'version': self.version, 'path': Path(f"MP/{self.name}")}


class App:
    def __init__(self, manager_object):
        self.mps = None
        self.manager = manager_object
        self.root = tk.Tk()
        self.root.title("Mod Manager")

        self.label = tk.Label(self.root, text='tags')
        self.label.pack()

        self.combobox = tk.ttk.Combobox(self.root, width=10)
        self.combobox.bind('<<ComboboxSelected>>', self.search)
        self.combobox.pack()

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack()

        self.load_button = tk.Button(self.root, text="Load ModPack", command=self.load_modpack)
        self.load_button.pack()

        self.create_button = tk.Button(self.root, text="Create modpack", command=self.create_modpack)
        self.create_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete)
        self.delete_button.pack()

        self.mps = {}
        self.combobox['values'] = (*self.combobox['values'], '')

        self.setup = tk.Button(self.root, text="Setup", command=self.setup)
        self.setup.pack()

        self.update_listbox()

    def setup(self):
        setuper = Setuper()
        setuper.root.grab_set()

    def delete(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No ModPack selected")
            return

        index = selection[0]
        modpack = self.manager.MPs[index]
        self.manager.delete_mp(modpack)
        messagebox.showinfo("Success", f"Deleted ModPack {modpack.name}")
        self.update_listbox()

    def run(self):
        self.root.mainloop()

    def search(self, data):
        self.listbox.delete(0, tk.END)
        if self.combobox.get() == '':
            self.update_listbox()

        else:
            for mp in self.mps[self.combobox.get()]:
                self.listbox.insert(tk.END, str(mp.name) + "  tags: " + ",".join(mp.tags))

    def create_modpack(self):
        create_window = CreateWindow(self.root)
        info: dict[str, str | list | Path] = create_window.open()
        mp = MP(info['name'], info['version'], info['path'], info['tags'])
        self.manager.add_mp(mp)
        mp.save_to_json()
        self.listbox.insert(tk.END, info['name'] + "  tags: " + ",".join(mp.tags))

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for mp in self.manager.MPs:
            self.listbox.insert(tk.END, str(mp.name) + "  tags: " + ", ".join(mp.tags))
            for tag in mp.tags:
                if tag is not None and tag != "":
                    if tag not in self.mps:
                        self.combobox['values'] = (*self.combobox['values'], tag)
                        self.mps[tag] = []

                    if mp not in self.mps[tag]:
                        self.mps[tag].append(mp)

        print(self.mps)

    def load_modpack(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No ModPack selected")
            return

        index = selection[0]
        modpack = self.manager.MPs[index]
        self.manager.change_mp(modpack)
        messagebox.showinfo("Success", f"Loaded ModPack {modpack.name}")


def load_mps_from_json(filename):
    if not os.path.exists(filename):
        with open(filename, 'w+') as f:
            json.dump({}, f)
        return []

    with open(filename, 'r') as f:
        data = json.load(f)

    mps = []
    for name, mp_data in data.items():
        mp = MP(name, mp_data["version"], mp_data["path"], mp_data["tags"])
        mps.append(mp)

    return mps


class Setuper:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.root = tk.Tk()
        self.root.title("setuper")

        self.label_minecraft = tk.Label(self.root, text="enter minecraft folder")
        self.label_minecraft.pack()

        self.entry_minecraft = tk.Entry(self.root, width=50)
        self.entry_minecraft.insert(tk.END, f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\.minecraft')
        self.entry_minecraft.pack()

        self.button = tk.Button(self.root, text="confirm", command=self.confirm)
        self.button.pack()

    def run(self):
        self.root.mainloop()

    def confirm(self):
        self.config['settings'] = {'minecraft': str(self.entry_minecraft.get())}
        with open('settings.ini', "w") as f:
            self.config.write(f)

        self.root.destroy()


def settings_reader():
    file = 'settings.ini'
    if not os.path.isfile(file):
        setuper = Setuper()
        setuper.run()
        if not os.path.isfile(file):
            return 'error'

    config = configparser.ConfigParser()
    config.read(file)
    return {'minecraft': config['settings']['minecraft']}


if __name__ == "__main__":
    settings = settings_reader()
    if not settings == 'error':
        manager = Manager(load_mps_from_json('MP.json'), minecraft_path=str(settings['minecraft']))
        app = App(manager)
        app.run()
