import json
import tkinter as tk
from tkinter import messagebox
from manager import Manager, MP


class App:
    def __init__(self, manager_object):
        self.manager = manager_object
        self.root = tk.Tk()
        self.root.title("Mod Manager")

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()

        self.load_button = tk.Button(self.root, text="Load ModPack", command=self.load_modpack)
        self.load_button.pack()

        self.update_listbox()

    def run(self):
        self.root.mainloop()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for mp in self.manager.MPs:
            self.listbox.insert(tk.END, mp.name)

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
    with open(filename, 'r') as f:
        data = json.load(f)

    mps = []
    for name, mp_data in data.items():
        mp = MP(name, mp_data["version"], mp_data["path"], mp_data["tags"])
        mps.append(mp)

    return mps


manager = Manager(load_mps_from_json('MP.json'))  # Здесь должен быть ваш список ModPacks
app = App(manager)
app.run()
