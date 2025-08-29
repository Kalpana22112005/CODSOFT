import tkinter as tk
from tkinter import messagebox
import json, os

FILE_NAME = "contacts.json"

def _normalize(data):
    """
    Accept old formats and return a list of dicts:
    [{'name':..., 'phone':..., 'email':..., 'address':...}, ...]
    """
    if isinstance(data, list):
        out = []
        for item in data:
            if not isinstance(item, dict):
                continue
            out.append({
                "name": str(item.get("name", "")),
                "phone": str(item.get("phone", "")),
                "email": str(item.get("email", "")),
                "address": str(item.get("address", "")),
            })
        return out

    if isinstance(data, dict):
    
        out = []
        for name, det in data.items():
            det = det or {}
            out.append({
                "name": str(name),
                "phone": str(det.get("phone", "")),
                "email": str(det.get("email", "")),
                "address": str(det.get("address", "")),
            })
        return out

    return []

def load_contacts():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return _normalize(json.load(f))
        except Exception:
         
            return []
    return []

def save_contacts():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

def refresh_listbox():
    """Rebuild listbox from current_view (mapping to real indices)."""
    listbox.delete(0, tk.END)
    for i in current_view:
        c = contacts[i]
        listbox.insert(tk.END, f"{c['name']} - {c['phone']}")

def show_all():
    """Show all contacts and reset search."""
    search_entry.delete(0, tk.END)
    current_view.clear()
    current_view.extend(range(len(contacts)))
    refresh_listbox()

def search_contact():
    q = search_entry.get().strip().lower()
    current_view.clear()
    for idx, c in enumerate(contacts):
        if q in c["name"].lower() or q in c["phone"]:
            current_view.append(idx)
    refresh_listbox()

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_text.delete("1.0", tk.END)

def on_select(_e=None):
    sel = listbox.curselection()
    if not sel:
        return
    real_idx = current_view[sel[0]]
    c = contacts[real_idx]
    clear_fields()
    name_entry.insert(0, c["name"])
    phone_entry.insert(0, c["phone"])
    email_entry.insert(0, c["email"])
    address_text.insert("1.0", c["address"])

def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_text.get("1.0", tk.END).strip()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone are required.")
        return

    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts()
    show_all()
    clear_fields()
    messagebox.showinfo("Success", "Contact added successfully!")

def update_contact():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select", "Select a contact to update.")
        return
    real_idx = current_view[sel[0]]

    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_text.get("1.0", tk.END).strip()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and Phone are required.")
        return

    contacts[real_idx] = {"name": name, "phone": phone, "email": email, "address": address}
    save_contacts()
    show_all()
    clear_fields()
    messagebox.showinfo("Updated", "Contact updated successfully!")

def delete_contact():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select", "Select a contact to delete.")
        return
    real_idx = current_view[sel[0]]
    nm = contacts[real_idx]["name"]
    if messagebox.askyesno("Confirm Delete", f"Delete '{nm}'?"):
        contacts.pop(real_idx)
        save_contacts()
        show_all()
        clear_fields()
        messagebox.showinfo("Deleted", "Contact deleted successfully!")

root = tk.Tk()
root.title("Contact Book")
root.state("zoomed")         
root.minsize(900, 520)      

title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12)
btn_font   = ("Helvetica", 11)

left = tk.Frame(root, padx=14, pady=10)
left.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(left, text="Contacts", font=title_font).pack(anchor="w", pady=(0, 6))

listbox = tk.Listbox(left, width=40, height=25, font=label_font)
listbox.pack(fill=tk.Y, pady=6)
listbox.bind("<<ListboxSelect>>", on_select)

search_entry = tk.Entry(left, font=label_font, width=24)
search_entry.pack(pady=(4, 2), anchor="w")
tk.Button(left, text="Search",  font=btn_font, width=12, command=search_contact).pack(anchor="w")
tk.Button(left, text="Show All", font=btn_font, width=12, command=show_all).pack(anchor="w", pady=(4, 0))

right = tk.Frame(root, padx=24, pady=20)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(right, text="Contact Book", font=title_font).grid(row=0, column=0, columnspan=2, pady=(0, 12))

tk.Label(right, text="Name:",   font=label_font).grid(row=1, column=0, sticky="w", pady=6)
name_entry = tk.Entry(right, font=label_font, width=34);  name_entry.grid(row=1, column=1, sticky="w")

tk.Label(right, text="Phone:",  font=label_font).grid(row=2, column=0, sticky="w", pady=6)
phone_entry = tk.Entry(right, font=label_font, width=34); phone_entry.grid(row=2, column=1, sticky="w")

tk.Label(right, text="Email:",  font=label_font).grid(row=3, column=0, sticky="w", pady=6)
email_entry = tk.Entry(right, font=label_font, width=34); email_entry.grid(row=3, column=1, sticky="w")

tk.Label(right, text="Address:",font=label_font).grid(row=4, column=0, sticky="nw", pady=6)
address_text = tk.Text(right, font=label_font, width=34, height=5); address_text.grid(row=4, column=1, sticky="w")

btns = tk.Frame(right, pady=18); btns.grid(row=5, column=0, columnspan=2)
tk.Button(btns, text="Add Contact",    font=btn_font, width=15, command=add_contact).grid(row=0, column=0, padx=6)
tk.Button(btns, text="Update Contact", font=btn_font, width=15, command=update_contact).grid(row=0, column=1, padx=6)
tk.Button(btns, text="Delete Contact", font=btn_font, width=15, command=delete_contact).grid(row=0, column=2, padx=6)
tk.Button(btns, text="Clear Fields",   font=btn_font, width=15, command=clear_fields).grid(row=0, column=3, padx=6)

contacts = load_contacts()    
current_view = list(range(len(contacts)))  
refresh_listbox()

root.mainloop()