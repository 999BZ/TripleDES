import tkinter as tk
from tkinter import filedialog, messagebox
import os

class TripleDesGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Triple DES Encryption/Decryption")
        self.master.geometry("900x700".format())

        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        x = (width - 900) // 2
        y = (height - 700) // 2
        self.master.geometry(f"900x700+{x}+{y}")

        self.master.configure(background='white')

        self.key_label = tk.Label(self.master, text="Key:",font=("Montserrat thin", 18),background='white')
        self.key_label.pack(pady=20)

        self.key_entry = tk.Entry(self.master, show="*",font=("Montserrat thin", 18),background='white')
        self.key_entry.pack()

        self.file_label = tk.Label(self.master, text="Select a file to encrypt/decrypt:",font=("Montserrat thin", 18),background='white')
        self.file_label.pack(pady=20)

        self.file_button = tk.Button(self.master, text="Browse",font=("Montserrat thin", 14),background='#007fff',foreground='white',activebackground="#0078D7",activeforeground="blue",borderwidth=0.5, relief='flat', padx=10, pady=10, command=self.select_file)
        self.file_button.pack()

    def select_file(self):
        #menu for file:
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
        if(self.filename != ""):
            self.file_label.config(text=self.filename)
        else:
            self.file_label.config(text="Select a file to encrypt/decrypt:")


if __name__ == "__main__":
    root = tk.Tk()
    gui = TripleDesGUI(root)
    root.mainloop()
