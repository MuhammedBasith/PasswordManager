import tkinter as tk  # import tkinter classes
# NOTE: messagebox is a separate module from tkinter which is not imported unless specified
from tkinter import messagebox
import pyperclip
import json
import generator

TITLE_FONT = ("Sergoe UI", 14, "bold")
PWD_FONT = ("Sergoe UI", 12, "bold")
NORMAL_FONT = ("Sergoe UI", 10, "normal")
LARGE_FONT = ("Sergoe UI", 12, "normal")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate():
    generator.get_list_of_chars()
    popup = generator.Popup(window)
    password = popup.password
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()

    new_data = {website: {"email": email, "password": password}}

    if len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showinfo(title="Error", message="Please fill in all fields.")
    else:
        response = messagebox.askokcancel(title="Please confirm", message=f"Website: {website}\nEmail: {email}\nPassword: {password}\n\nOK to save?")
        if response:
            try:
                # encoding="utf-16" allows extended unicode characters to be written to file
                # Read from JSON file:
                with open("data.json", mode="r", encoding="utf-8") as file:
                    data = json.load(fp=file)
            except FileNotFoundError:
                # Create a new JSON data dictionary from new_data
                data = new_data
            else:
                # Update existing JSON data dictionary with new_data:
                data.update(new_data)
            finally:
                # Dump the JSON data dictionary to file:
                with open("data.json", mode="w", encoding="utf-8") as file:
                    json.dump(data, fp=file, indent=4)
                # Delete the entries in the GUI
                entry_website.delete(0, tk.END)
                entry_password.delete(0, tk.END)


# ---------------------------- SEARCH WEBSITE ------------------------------- #

def search():
    website = entry_website.get()

    try:
        # encoding="utf-16" allows extended unicode characters to be written to file
        # Read from JSON file:
        with open("data.json", mode="r", encoding="utf-8") as file:
            data = json.load(fp=file)
    except FileNotFoundError:
        # Pop-up messagebox
        messagebox.showinfo(title="File Not Found",
                            message="Cannot find file 'data.json'.\nThere are no passwords saved.")
    else:
        # try:
        #     # Retrieve the website data
        #     email = data[website]["email"]
        #     password = data[website]["password"]
        # except KeyError:
        #     # Pop-up messagebox
        #     messagebox.showinfo(title=website, message=f"Website {website} not found in file 'data.json'")
        # else:
        #     # Pop-up messagebox
        #     messagebox.showinfo(title=website, message=f"Email: \t\t{email}\nPassword: \t{password}")
        # finally:
        #     # Delete the entries in the GUI
        #     entry_website.delete(0, tk.END)
        #     entry_password.delete(0, tk.END)

        # Only use try/except block if there is no other easy way to achieve the same result
        if website in file:
            email = data[website]["email"]
            password = data[website]["password"]
            # Pop-up messagebox
            messagebox.showinfo(title=website, message=f"Email: \t\t{email}\nPassword: \t{password}")
        else:
            # Pop-up messagebox
            messagebox.showinfo(title=website, message=f"Website {website} not found in file 'data.json'")
        # Delete the entries in the GUI
        entry_website.delete(0, tk.END)
        entry_password.delete(0, tk.END)


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = tk.Canvas(window, width=200, height=200)
image = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)

label_website = tk.Label(window, text="Website:")
label_email = tk.Label(window, text="Email / Username:")
label_password = tk.Label(window, text="Password:")

entry_website = tk.Entry(window, width=21)
entry_website.focus()
entry_email = tk.Entry(window, width=35)
entry_email.insert(0, "example@gmail.com")  # Inserts string just before the character indicated by index.
entry_password = tk.Entry(window, width=21)

button_search = tk.Button(window, text="Search", command=search)
button_generate = tk.Button(window, text="Generate Password", command=generate)
button_add = tk.Button(window, text="Add", width=36, command=save)


# Grid layout
canvas.grid(row=0, column=1)
label_website.grid(row=1, column=0, sticky=tk.E)
label_email.grid(row=2, column=0, sticky=tk.E)
label_password.grid(row=3, column=0, sticky=tk.E)
entry_website.grid(row=1, column=1, sticky=tk.EW)
entry_email.grid(row=2, column=1, columnspan=2, sticky=tk.EW)
entry_password.grid(row=3, column=1, sticky=tk.EW)
button_search.grid(row=1, column=2, sticky=tk.EW)
button_generate.grid(row=3, column=2, sticky=tk.EW)
button_add.grid(row=4, column=1, columnspan=2, sticky=tk.EW)


# ---------------------

window.mainloop()
