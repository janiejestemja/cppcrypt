import tkinter as tk
from tkinter import filedialog

def main():
    print("Starting app...")

    # Init window
    root = tk.Tk()
    root.title("Tkinter GUI")
    root.geometry("1200x1200")
    # Open button for file
    choose_file_button = tk.Button(root, text="Open File", command=lambda: choose_file(text_area))
    choose_file_button.grid(row=0, column=0)

    pw_entry = tk.Entry(root)
    pw_entry.grid(row=0, column=1)

    crypt_button = tk.Button(root, text="Decrypt", command=lambda: show_password(pw_entry))
    crypt_button.grid(row=0, column=2)

    text_area = tk.Text(root, wrap="word", width=60, font=("Arial", 12))
    text_area.grid(row=1, columns=3) 
    # Starting app
    root.mainloop()

# Helperfunctions (development...)
def show_password(pw_entry):
    print(pw_entry.get())

def on_buttonclick():
    print("Button Clicked!")

def on_key(event):
    print("Key pressed: ", event.char)

# Display a textile
def choose_file(text_area):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path) as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())

if __name__ == "__main__":
    main()
