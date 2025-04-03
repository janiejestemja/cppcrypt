import os

import numpy as np
import tkinter as tk
from tkinter import filedialog

from pyaes import aes_encrypt, key_expansion
from cryptology.utils import check_passkey, load_file, save_crypt, str_to_states

infile_path = ""
default_passkey = "0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f"
outfile_defaultname = "crypt.txt"

def main():
    print("Starting app...")

    # Init window
    root = tk.Tk()
    root.title("Tkinter GUI")
    root.geometry("1280x800")

    # Actions
    actions_frame = tk.Frame(root)
    actions_frame.pack(side="top", padx=10, pady=10, fill="both")

    # Open button for file
    choose_file_button = tk.Button(actions_frame, text="Open File", command=lambda: choose_infile(text_area))
    choose_file_button.pack(side="left")

    # Encryption button
    encrypt_btn = tk.Button(actions_frame, text="Encrypt opened File", command=lambda: encrypt_txt(pw_entry, text_area))
    encrypt_btn.pack(side="left")

     # Decryption button
    decrypt_btn = tk.Button(actions_frame, text="Decrypt Text", command=lambda: decrypt_txt(pw_entry, text_area))
    decrypt_btn.pack(side="left")

   # Save button
    save_btn = tk.Button(actions_frame, text="Save Text", command=lambda: save_txt(text_area))
    save_btn.pack(side="left")

    # Frame for passkey
    passkey_frame = tk.Frame(root)
    passkey_frame.pack(side="top", padx=10, pady=10, fill="both")

    # Label for passkey input
    pw_label = tk.Label(passkey_frame, text="Passkey: ")
    pw_label.pack(side="left")

    # Textinput for passkey
    pw_entry = tk.Entry(passkey_frame, width=32)
    pw_entry.pack(side="left")

    # Frame for Textfile
    frame = tk.Frame(root)
    frame.pack(side="top", padx=10, pady=10, fill="both")

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    
    text_area = tk.Text(frame, wrap="word", font=("Arial", 10), yscrollcommand=scrollbar.set)
    text_area.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=text_area.yview)

    # Starting app
    root.mainloop()

    print("App ended.")

# Helperfunctions
def encrypt_txt(pw_entry, text_area):
    passkey = pw_entry.get()

    if passkey == "":
        passkey = default_passkey

    if check_passkey(passkey) == False:
        print("Passkey check failed")
        return None

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if file_path:
        text = text_area.get("1.0", "end-1c")
        states = str_to_states(text)
        round_keys = key_expansion(bytes([int(ele, 16) for ele in passkey.split(",")]))

        cipherstates = []
        for state in states:
            cipherstates.append(aes_encrypt(state, round_keys))

        save_crypt(file_path, cipherstates)

        print("File saved at: ", file_path)

def decrypt_txt(pw_entry, text_area):
    passkey = pw_entry.get()

    if passkey == "":
        passkey = default_passkey

    if check_passkey(passkey) == False:
        print("Passkey check failed")
        return None

    if infile_path != "":
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, load_file(crypt_name=infile_path, passkey=passkey))

def save_txt(text_area):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(text_area.get("1.0", "end-1c"))
        
        print("File saved")

# Display a textile
def choose_infile(text_area):
    global infile_path

    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path) as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())

        infile_path = file_path

if __name__ == "__main__":
    main()
