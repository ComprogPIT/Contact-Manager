import tkinter as tk
from tkinter import messagebox

FILE = "contacts.txt"


def load_contacts():
    try:
        with open(FILE, "r") as f:
            lines = f.readlines()
        contacts = []
        for line in lines:
            parts = line.strip().split("|")
            if len(parts) == 3:
                contacts.append(parts)
        return contacts
    except FileNotFoundError:
        return []


def save_contacts():
    with open(FILE, "w") as f:
        for c in contacts:
            f.write(c[0] + "|" + c[1] + "|" + c[2] + "\n")


def show_contacts():
    listbox.delete(0, tk.END)
    for c in contacts:
        listbox.insert(tk.END, c[0] + "  |  " + c[1] + "  |  " + c[2])


def add_contact():
    name = entry_name.get()
    number = entry_number.get()
    address = entry_address.get()

    if name == "" or number == "" or address == "":
        messagebox.showwarning("Error", "All fields are required.")
        return

    contacts.append([name, number, address])
    save_contacts()
    show_contacts()
    clear_fields()


def update_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select a contact first.")
        return

    index = selected[0]
    contacts[index][0] = entry_name.get()
    contacts[index][1] = entry_number.get()
    contacts[index][2] = entry_address.get()
    save_contacts()
    show_contacts()
    clear_fields()


def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Select a contact first.")
        return

    index = selected[0]
    confirm = messagebox.askyesno("Confirm", "Delete this contact?")
    if confirm:
        contacts.pop(index)
        save_contacts()
        show_contacts()
        clear_fields()


def search_contact():
    keyword = entry_search.get().lower()
    listbox.delete(0, tk.END)
    for c in contacts:
        if keyword in c[0].lower() or keyword in c[1] or keyword in c[2].lower():
            listbox.insert(tk.END, c[0] + "  |  " + c[1] + "  |  " + c[2])


def select_contact(event):
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    clear_fields()
    entry_name.insert(0, contacts[index][0])
    entry_number.insert(0, contacts[index][1])
    entry_address.insert(0, contacts[index][2])


def clear_fields():
    entry_name.delete(0, tk.END)
    entry_number.delete(0, tk.END)
    entry_address.delete(0, tk.END)


contacts = load_contacts()

window = tk.Tk()
window.title("Contact Manager")
window.geometry("500x480")

tk.Label(window, text="Name:").pack()
entry_name = tk.Entry(window, width=40)
entry_name.pack()

tk.Label(window, text="Number:").pack()
entry_number = tk.Entry(window, width=40)
entry_number.pack()

tk.Label(window, text="Address:").pack()
entry_address = tk.Entry(window, width=40)
entry_address.pack()

tk.Button(window, text="Add", command=add_contact, width=12).pack(pady=2)
tk.Button(window, text="Update", command=update_contact, width=12).pack(pady=2)
tk.Button(window, text="Delete", command=delete_contact, width=12).pack(pady=2)
tk.Button(window, text="Clear", command=clear_fields, width=12).pack(pady=2)

tk.Label(window, text="Search:").pack()
entry_search = tk.Entry(window, width=40)
entry_search.pack()
tk.Button(window, text="Search", command=search_contact, width=12).pack(pady=2)

listbox = tk.Listbox(window, width=65, height=8)
listbox.pack(pady=5)
listbox.bind("<<ListboxSelect>>", select_contact)

show_contacts()
window.mainloop()