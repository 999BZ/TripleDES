import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import os
import binascii
from binascii import hexlify,unhexlify

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

        # radio buttons:
        self.action_label = tk.Label(self.master, text="Select an action:",font=("Montserrat thin", 18),background='white')
        self.action_label.pack(pady=20)
        self.action_var = tk.StringVar()
        self.action_var.set("encrypt")
        self.encrypt_radio = tk.Radiobutton(self.master, text="Encrypt", variable=self.action_var, value="encrypt",font=("Montserrat thin", 14),background='white')
        self.encrypt_radio.pack()
        self.decrypt_radio = tk.Radiobutton(self.master, text="Decrypt", variable=self.action_var, value="decrypt",font=("Montserrat thin", 14),background='white')
        self.decrypt_radio.pack()

        self.submit_button = tk.Button(self.master, text="Submit", font=("Montserrat thin", 14),background='white', command=self.start)
        self.submit_button.pack(pady=20)

        #initialization vector:
        self.iv = os.urandom(DES3.block_size)

    def select_file(self):
        #menu for file:
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
        if(self.filename != ""):
            self.file_label.config(text=self.filename)
        else:
            self.file_label.config(text="Select a file to encrypt/decrypt:")



    def start(self):
        # get the key:
        key = self.key_entry.get().encode('utf-8')
        if not key:
            messagebox.showerror("Error", "Please enter a key.")
            return
        #padding the key:
        key = pad(key, DES3.block_size*2, style='pkcs7')

        #see if a file has been selected:
        try:
            with open(self.filename, "rb") as f:
                data = f.read()
        except AttributeError:
            messagebox.showerror("Error", "Please select a file.")
            return

        #get action of either Encryption or Decryption from the form:
        action = self.action_var.get()

        #encryption:
        if action == "encrypt":
            iv = os.urandom(DES3.block_size)
            cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
            ciphertext = binascii.hexlify(cipher.encrypt(pad(data, DES3.block_size, style='pkcs7')))
            output_filename = os.path.splitext(self.filename)[0] + "_encrypted" + os.path.splitext(self.filename)[1]
            iv_hex = hexlify(iv)
            ciphertext = iv_hex + ciphertext
        else:
            #decryption
            iv_hex = data[:DES3.block_size2].decode('utf-8')
            iv = binascii.unhexlify(iv_hex)
            cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(binascii.unhexlify(data[DES3.block_size2:])), DES3.block_size, style='pkcs7')
            output_extension = os.path.splitext(self.filename)[1]
            if output_extension == ".txt":
                output_filename = os.path.splitext(self.filename)[0] + "_decrypted.txt"
            else:
                output_filename = os.path.splitext(self.filename)[0] + "_decrypted" + output_extension

        #output the file
        with open(output_filename, "wb") as f:
            f.write(ciphertext if action == "encrypt" else plaintext)

        #indicator that everything went as planned
        messagebox.showinfo("Complete", "Operation complete. Output file: " + output_filename)
        
if __name__ == "__main__":
    root = tk.Tk()
    gui = TripleDesGUI(root)
    root.mainloop()
