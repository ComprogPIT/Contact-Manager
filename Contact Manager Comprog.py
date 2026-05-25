import tkinter as tk
from tkinter import messagebox
import os

FILE_NAME = "contacts.txt"

# ================= WINDOW =================
root = tk.Tk()
root.title("Contact Manager Pro")
root.geometry("850x600")
root.resizable(False, False)

# ================= GRADIENT =================
canvas = tk.Canvas(root, width=850, height=600)
canvas.place(x=0, y=0)

for i in range(600):
    r = int(10 + i * 0.08)
    g = int(10 + i * 0.06)
    b = 0
    color = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, 850, i, fill=color)

# ================= FRAME =================
frame = tk.Frame(root, bg="#111111")
frame.place(x=60, y=40, width=730, height=520)

# ================= TITLE =================
tk.Label(
    frame,
    text="CONTACT MANAGER PRO",
    font=("Arial", 20, "bold"),
    fg="#FFD700",
    bg="#111111"
).pack(pady=10)

# ================= INPUT =================
form = tk.Frame(frame, bg="#111111")
form.pack(pady=10)

tk.Label(form, text="Name", fg="white", bg="#111111").grid(row=0, column=0, sticky="w")
tk.Label(form, text="Number", fg="white", bg="#111111").grid(row=1, column=0, sticky="w")
tk.Label(form, text="Address", fg="white", bg="#111111").grid(row=2, column=0, sticky="w")

name_entry = tk.Entry(form, width=35, bg="#222222", fg="white", insertbackground="white")
number_entry = tk.Entry(form, width=35, bg="#222222", fg="white", insertbackground="white")
address_entry = tk.Entry(form, width=35, bg="#222222", fg="white", insertbackground="white")

name_entry.grid(row=0, column=1, padx=10, pady=5)
number_entry.grid(row=1, column=1, padx=10, pady=5)
address_entry.grid(row=2, column=1, padx=10, pady=5)

# ================= FILE FUNCTIONS =================
def read_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return [i.strip() for i in f.readlines()]


def write_contacts(data):
    with open(FILE_NAME, "w") as f:
        for i in data:
            f.write(i + "\n")

# ================= FUNCTIONS =================
def load_contacts():
    listbox.delete(0, tk.END)
    for c in read_contacts():
        listbox.insert(tk.END, c)


def add_contact():
    n = name_entry.get()
    num = number_entry.get()
    addr = address_entry.get()

    if n == "" or num == "" or addr == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    if not num.isdigit():
        messagebox.showerror("Error", "Number only")
        return

    data = read_contacts()
    data.append(n + "|" + num + "|" + addr)
    write_contacts(data)

    load_contacts()
    clear_fields()


def delete_contact():
    sel = listbox.curselection()
    if not sel:
        return

    contact = listbox.get(sel[0])
    data = read_contacts()

    if contact in data:
        data.remove(contact)

    write_contacts(data)
    load_contacts()
    clear_fields()


def update_contact():
    sel = listbox.curselection()
    if not sel:
        return

    old = listbox.get(sel[0])
    new = name_entry.get() + "|" + number_entry.get() + "|" + address_entry.get()

    data = read_contacts()

    for i in range(len(data)):
        if data[i] == old:
            data[i] = new

    write_contacts(data)
    load_contacts()
    clear_fields()


def search_contact():
    key = name_entry.get().lower()
    listbox.delete(0, tk.END)

    for c in read_contacts():
        if key in c.lower():
            listbox.insert(tk.END, c)


def select_contact(event):
    sel = listbox.curselection()
    if not sel:
        return

    data = listbox.get(sel[0]).split("|")

    clear_fields()
    name_entry.insert(0, data[0])
    number_entry.insert(0, data[1])
    address_entry.insert(0, data[2])


def clear_fields():
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# ================= BUTTONS =================
btn_frame = tk.Frame(frame, bg="#111111")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="ADD", command=add_contact, width=10, bg="#FFD700").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="UPDATE", command=update_contact, width=10, bg="#FFD700").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="DELETE", command=delete_contact, width=10, bg="#FFD700").grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="SEARCH", command=search_contact, width=10, bg="#FFD700").grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="VIEW", command=load_contacts, width=10, bg="#FFD700").grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="CLEAR", command=clear_fields, width=10, bg="#FFD700").grid(row=0, column=5, padx=5)

# ================= LISTBOX =================
listbox = tk.Listbox(frame, width=80, height=15, bg="#1a1a1a", fg="white",
                     selectbackground="#FFD700", selectforeground="black")
listbox.pack(pady=10)

listbox.bind("<<ListboxSelect>>", select_contact)

# ================= START =================
load_contacts()
root.mainloop()