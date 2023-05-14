import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import DES
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

        self.key1_label = tk.Label(self.master, text="Key 1 (MAX 8 char):",font=("Montserrat thin", 18),background='white')
        self.key1_label.pack(pady=20)

        self.key1_entry = tk.Entry(self.master, show="*",font=("Montserrat thin", 18),background='white')
        self.key1_entry.pack()

        self.key2_label = tk.Label(self.master, text="Key 2 (MAX 8 char):",font=("Montserrat thin", 18),background='white')
        self.key2_label.pack(pady=20)

        self.key2_entry = tk.Entry(self.master, show="*",font=("Montserrat thin", 18),background='white')
        self.key2_entry.pack()

        self.file_label = tk.Label(self.master, text="Select a file to encrypt/decrypt:",font=("Montserrat thin", 18),background='white')
        self.file_label.pack(pady=20)

        self.file_button = tk.Button(self.master, text="Browse", font=("Montserrat thin", 14),background='#007fff',foreground='white',activebackground="#0078D7",activeforeground="blue",borderwidth=0.5, relief='flat', padx=10, pady=10, command=self.select_file)
        self.file_button.pack()

        #radio buttons:
        self.action_label = tk.Label(self.master, text="Select an action:",font=("Montserrat thin", 18),background='white')
        self.action_label.pack(pady=20)
        self.action_var = tk.StringVar()
        self.action_var.set("encrypt")
        self.encrypt_radio = tk.Radiobutton(self.master, text="Encrypt", variable=self.action_var, value="encrypt",font=("Montserrat thin", 14),background='white')
        self.encrypt_radio.pack()
        self.decrypt_radio = tk.Radiobutton(self.master, text="Decrypt", variable=self.action_var, value="decrypt",font=("Montserrat thin", 14),background='white')
        self.decrypt_radio.pack()

        #start encryption/decryption:
        self.submit_button = tk.Button(self.master, text="Submit", font=("Montserrat thin", 14),background='white', command=self.start)
        self.submit_button.pack(pady=20)


    def select_file(self):
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
        if (self.filename != ""):
            self.file_label.config(text=self.filename)
        else:
            self.file_label.config(text="Select a file to encrypt/decrypt:")


    def start(self):
        # get the key
        key1 = self.key1_entry.get().encode('utf-8')
        key2 = self.key2_entry.get().encode('utf-8')
        if not key1 :
            messagebox.showerror("Error", "Please enter key 1.")
            return
        if not key2 :
            messagebox.showerror("Error", "Please enter key 2.")
            return
        if (len(key1)>8):
            messagebox.showerror("Error", "Key 1 is too long.")
            return
        if (len(key2)>8):
            messagebox.showerror("Error", "Key 2 is too long.")
            return
        if (len(key1) < 8):
            key1 = pad(key1, DES.block_size, style='pkcs7')
        if (len(key2) < 8):
            key2 = pad(key2, DES.block_size, style='pkcs7')


        try:
            #if button browse is clicked:
            if(self.filename != ""):
                with open(self.filename, "rb") as f:
                    data = f.read()
            else:
                messagebox.showerror("Error", "Please select a file.")
                return
        except AttributeError:
            #if button browse isn't clicked:
            messagebox.showerror("Error", "Please select a file.")
            return


        #get action to encrypt or decrypt
        action = self.action_var.get()

        #encryption:
        if action == "encrypt":
            ciphertext = self.Encryption(data,key1,key2)
            output_filename = os.path.splitext(self.filename)[0] + "_encrypted" + os.path.splitext(self.filename)[1]
        else:
        #decryption:
            plaintext = self.Decryption(data,key1,key2)
            if (plaintext == ""):
                return
            output_extension = os.path.splitext(self.filename)[1]
            if output_extension == ".txt":
                output_filename = os.path.splitext(self.filename)[0] + "_decrypted.txt"
            else:
                output_filename = os.path.splitext(self.filename)[0] + "_decrypted" + output_extension

        #write new file encrypted or decrypted:
        with open(output_filename, "wb") as f:
            f.write(ciphertext if action == "encrypt" else plaintext)

        # show a message box to indicate completion
        messagebox.showinfo("Complete", "Operation complete. Output file: " + output_filename)
    def Encryption(self,data,key1,key2):
        iv = os.urandom(DES.block_size)

        padded_data = pad(data,DES.block_size)

        firstDES = self.encrypt_DES(padded_data,key1,iv)

        secondDES = self.decrypt_DES(firstDES,key2,iv)

        thirdDES = self.encrypt_DES(secondDES,key1,iv)

        # Combine the IV and ciphertext into a single bytes object
        iv_hex = binascii.hexlify(iv)
        ciphertext_hex = binascii.hexlify(thirdDES)
        result = iv_hex + ciphertext_hex

        return result

    def Decryption(self,data,key1,key2):
        try:
            # Extract the IV and ciphertext from the input data
            iv_hex = data[:DES.block_size*2].decode('utf-8')
        except UnicodeDecodeError:
            messagebox.showerror("Error", "Decryption failed. File encoding not supported.")
            plainText = ""
            return plainText

        try:
            iv = binascii.unhexlify(iv_hex)
        except binascii.Error:
            messagebox.showerror("Error", "Decryption failed. Please select an encrypted file.")
            plainText = ""
            return plainText

        ciphertext = binascii.unhexlify(data[DES.block_size*2:])

        firstDES = self.decrypt_DES(ciphertext,key1,iv)

        secondDES = self.encrypt_DES(firstDES,key2,iv)

        thirdDES = self.decrypt_DES(secondDES,key1,iv)

        try:
            plainText = unpad(thirdDES,DES.block_size)
        except ValueError:
            messagebox.showerror("Error", "Decryption failed. Incorrect key combination was used.")
            plainText = ""
            return plainText
        return plainText

    def encrypt_DES(self,data,key,iv):
        cipher = DES.new(key,DES.MODE_CBC,iv=iv)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def decrypt_DES(self,cipherData,key,iv):
        cipher = DES.new(key,DES.MODE_CBC,iv=iv)
        plaintext = cipher.decrypt(cipherData)
        return plaintext

if __name__ == "__main__":
    root = tk.Tk()
    gui = TripleDesGUI(root)
    root.mainloop()
