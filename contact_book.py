import tkinter as tk
from tkinter import messagebox
import json
import os
FILE_NAME = "contacts.json"
# ---------------- Load Contacts ----------------
def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []
# ---------------- Save Contacts ----------------
def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)
# ---------------- Refresh Contact List ----------------
def refresh_list(data=None):
    contact_list.delete(0, tk.END)
    if data is None:
        data = contacts
    for contact in data:
        contact_list.insert(
            tk.END,
            f"{contact['name']}   |   {contact['phone']}"
        )
# ---------------- Clear Fields ----------------
def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
# ---------------- Add Contact ----------------
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()
    if name == "" or phone == "":
        messagebox.showwarning(
            "Warning",
            "Name and Phone Number are required."
        )
        return
    for contact in contacts:
        if contact["phone"] == phone:
            messagebox.showwarning(
                "Duplicate",
                "Phone number already exists."
            )
            return
    contacts.append(
        {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
    )
    save_contacts()
    refresh_list()
    clear_fields()
    messagebox.showinfo(
        "Success",
        "Contact Added Successfully."
    )
# ---------------- Main Window ----------------
window = tk.Tk()
window.title("Contact Book")
window.geometry("700x800")
window.config(bg="#F4F4F4")
window.resizable(False, False)
contacts = load_contacts()
# ---------------- Heading ----------------
title = tk.Label(
    window,
    text="CONTACT BOOK",
    font=("Arial",20,"bold"),
    fg="navy",
    bg="#F4F4F4"
)
title.pack(pady=15)
# ---------------- Name ----------------
tk.Label(
    window,
    text="Name",
    bg="#F4F4F4",
    font=("Arial",11)
).pack()
name_entry = tk.Entry(
    window,
    width=40,
    font=("Arial",11)
)
name_entry.pack(pady=5)
# ---------------- Phone ----------------
tk.Label(
    window,
    text="Phone Number",
    bg="#F4F4F4",
    font=("Arial",11)
).pack()
phone_entry = tk.Entry(
    window,
    width=40,
    font=("Arial",11)
)
phone_entry.pack(pady=5)
# ---------------- Email ----------------
tk.Label(
    window,
    text="Email",
    bg="#F4F4F4",
    font=("Arial",11)
).pack()
email_entry = tk.Entry(
    window,
    width=40,
    font=("Arial",11)
)
email_entry.pack(pady=5)
# ---------------- Address ----------------
tk.Label(
    window,
    text="Address",
    bg="#F4F4F4",
    font=("Arial",11)
).pack()
address_entry = tk.Entry(
    window,
    width=40,
    font=("Arial",11)
)
address_entry.pack(pady=5)
# ---------------- Add Button ----------------
add_button = tk.Button(
    window,
    text="Add Contact",
    bg="green",
    fg="white",
    width=18,
    font=("Arial",11,"bold"),
    command=add_contact
)
add_button.pack(pady=12)
# ---------------- Contact List ----------------
contact_list = tk.Listbox(
    window,
    width=60,
    height=12,
    font=("Arial",11)
)
contact_list.pack(pady=10)
refresh_list()
# ---------------- Search Contact ----------------
def search_contact():
    keyword = search_entry.get().strip().lower()
    if keyword == "":
        refresh_list()
        return
    result = []
    for contact in contacts:
        if (keyword in contact["name"].lower()) or (keyword in contact["phone"]):
            result.append(contact)
    if result:
        refresh_list(result)
    else:
        contact_list.delete(0, tk.END)
        messagebox.showinfo(
            "Search",
            "No Contact Found."
        )
# ---------------- Show All Contacts ----------------
def show_all():
    search_entry.delete(0, tk.END)
    refresh_list()
# ---------------- Search Section ----------------
search_frame = tk.Frame(
    window,
    bg="#F4F4F4"
)
search_frame.pack(pady=10)
search_label = tk.Label(
    search_frame,
    text="Search",
    bg="#F4F4F4",
    font=("Arial",11)
)
search_label.grid(row=0,column=0,padx=5)
search_entry = tk.Entry(
    search_frame,
    width=25,
    font=("Arial",11)
)
search_entry.grid(row=0,column=1,padx=5)
search_button = tk.Button(
    search_frame,
    text="Search",
    bg="blue",
    fg="white",
    width=10,
    command=search_contact
)
search_button.grid(row=0,column=2,padx=5)
show_button = tk.Button(
    search_frame,
    text="Show All",
    bg="orange",
    fg="white",
    width=10,
    command=show_all
)
show_button.grid(row=0,column=3,padx=5)
# ---------------- Fill Entries ----------------
def fill_entries(event):
    selected = contact_list.curselection()
    if not selected:
        return
    selected_text = contact_list.get(selected[0])
    phone = selected_text.split("|")[1].strip()
    for contact in contacts:
        if contact["phone"] == phone:
            clear_fields()
            name_entry.insert(0, contact["name"])
            phone_entry.insert(0, contact["phone"])
            email_entry.insert(0, contact["email"])
            address_entry.insert(0, contact["address"])
            break
contact_list.bind("<<ListboxSelect>>", fill_entries)
# ---------------- Update Contact ----------------
def update_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a contact."
        )
        return
    old_phone = contact_list.get(selected[0]).split("|")[1].strip()
    for contact in contacts:
        if contact["phone"] == old_phone:
            contact["name"] = name_entry.get().strip()
            contact["phone"] = phone_entry.get().strip()
            contact["email"] = email_entry.get().strip()
            contact["address"] = address_entry.get().strip()
            break
    save_contacts()
    refresh_list()
    clear_fields()
    messagebox.showinfo(
        "Success",
        "Contact Updated Successfully."
    )
# ---------------- Delete Contact ----------------
def delete_contact():
    selected = contact_list.curselection()
    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a contact."
        )
        return
    phone = contact_list.get(selected[0]).split("|")[1].strip()
    for contact in contacts:
        if contact["phone"] == phone:
            contacts.remove(contact)
            break
    save_contacts()
    refresh_list()
    clear_fields()
    messagebox.showinfo(
        "Deleted",
        "Contact Deleted Successfully."
    )
# ---------------- Bottom Buttons ----------------
button_frame = tk.Frame(
    window,
    bg="#F4F4F4"
)
button_frame.pack(pady=10)
update_button = tk.Button(
    button_frame,
    text="Update",
    bg="green",
    fg="white",
    width=12,
    font=("Arial",10,"bold"),
    command=update_contact
)
update_button.grid(row=0,column=0,padx=5)
delete_button = tk.Button(
    button_frame,
    text="Delete",
    bg="red",
    fg="white",
    width=12,
    font=("Arial",10,"bold"),
    command=delete_contact
)
delete_button.grid(row=0,column=1,padx=5)
# ---------------- Run Application ----------------
window.mainloop()