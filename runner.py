import tkinter as tk
from tkinter import filedialog

from cryptology.utils import check_passkey, load_files

default_passkey = "0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f"

def main():
    print("Starting app...")

    # Init window
    root = tk.Tk()
    root.title("Tkinter GUI")
    root.geometry("1280x800")


    navbar = tk.Frame(root)
    navbar.pack(side="top", padx=10, pady=10, fill="both")

    # Open button for file
    choose_file_button = tk.Button(navbar, text="Open File", command=lambda: choose_file(text_area))
    choose_file_button.pack(side="left")

    pw_entry = tk.Entry(navbar, width=32)
    pw_entry.pack(side="left")

    crypt_button = tk.Button(navbar, text="Decrypt", command=lambda: show_password(pw_entry, text_area))
    crypt_button.pack(side="left")

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

# Helperfunctions (development...)
def show_password(pw_entry, text_area):
    global crypt_path
    passkey = pw_entry.get()
    print(passkey)
    if passkey == "":
        passkey = default_passkey
    if check_passkey(passkey) == False:
        print("Passkey check failed")
    else:
        if crypt_path != "":
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, load_files(crypt_name=crypt_path, passkey=passkey))
    
crypt_path = ""
# Display a textile
def choose_file(text_area):
    global crypt_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path) as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())
        crypt_path = file_path


if __name__ == "__main__":
    main()
