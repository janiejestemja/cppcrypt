import tkinter as tk
from tkinter import filedialog

from cryptology.utils import check_passkey, load_files

infile_path = ""
default_passkey = "0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f"

def main():
    print("Starting app...")

    # Init window
    root = tk.Tk()
    root.title("Tkinter GUI")
    root.geometry("1280x800")

    # Navigation bar 
    navbar = tk.Frame(root)
    navbar.pack(side="top", padx=10, pady=10, fill="both")

    # Open button for file
    choose_file_button = tk.Button(navbar, text="Open File", command=lambda: choose_file(text_area))
    choose_file_button.pack(side="left")

    # Textinput for passkey
    pw_entry = tk.Entry(navbar, width=32)
    pw_entry.pack(side="left")

    # Encryption button
    encrypt_btn = tk.Button(navbar, text="Encrypt", command=lambda: encrypt_txt(pw_entry))
    encrypt_btn.pack(side="left")

    # Decryption button
    decrypt_btn = tk.Button(navbar, text="Decrypt", command=lambda: decrypt_txt(pw_entry, text_area))
    decrypt_btn.pack(side="left")

    # Create frame for scrollbar and text
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
def encrypt_txt(pw_entry):
    print("Not implemented")

def decrypt_txt(pw_entry, text_area):
    passkey = pw_entry.get()

    if passkey == "":
        passkey = default_passkey

    if check_passkey(passkey) == False:
        print("Passkey check failed")
        return None

    if infile_path != "":
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, load_files(crypt_name=infile_path, passkey=passkey))

# Display a textile
def choose_file(text_area):
    global infile_path

    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path) as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())

        infile_path = file_path


if __name__ == "__main__":
    main()
