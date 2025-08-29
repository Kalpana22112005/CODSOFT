import tkinter as tk
from tkinter import messagebox
import json, os

FILE = "tasks.json"

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                out = []
                for item in data:
                    if isinstance(item, dict):
                        out.append({"text": str(item.get("text","")), "done": bool(item.get("done", False))})
                    else:
                        out.append({"text": str(item), "done": False})
                return out
        except:
            pass
    return []

def save():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def refresh(view=None):
    listbox.delete(0, tk.END)
    data = view if view is not None else tasks
    for t in data:
        prefix = "✔ " if t["done"] else "• "
        listbox.insert(tk.END, prefix + t["text"])

def add_task():
    txt = entry.get().strip()
    if not txt:
        return
    tasks.append({"text": txt, "done": False})
    save()
    entry.delete(0, tk.END)
    refresh()

def delete_task():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("⚠️ Warning", "Please select a task to delete!")
        return
    idx = sel[0]
    if messagebox.askyesno("Delete", f"Delete: {tasks[idx]['text']}?"):
        tasks.pop(idx)
        save()
        refresh()

def toggle_done():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("⚠️ Warning", "Please select a task to mark as done/undone!")
        return
    idx = sel[0]
    tasks[idx]["done"] = not tasks[idx]["done"]
    save()
    refresh()

def edit_task():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("⚠️ Warning", "Please select a task to edit!")
        return
    idx = sel[0]
    new = entry.get().strip()
    if not new:
        messagebox.showwarning("⚠️ Warning", "Please enter new text to edit the task!")
        return
    tasks[idx]["text"] = new
    save()
    entry.delete(0, tk.END)
    refresh()

def clear_input():
    entry.delete(0, tk.END)

def search():
    q = search_entry.get().lower().strip()
    view = [t for t in tasks if q in t["text"].lower()]
    refresh(view)

def show_all():
    search_entry.delete(0, tk.END)
    refresh()

root = tk.Tk()
root.title("To-Do List")
root.geometry("800x480")
root.minsize(720, 420)

title = tk.Label(root, text="📝 To-Do List", font=("Segoe UI", 16, "bold"))
title.pack(pady=(10, 6))

top = tk.Frame(root)
top.pack(padx=12, fill="x")

entry = tk.Entry(top, font=("Segoe UI", 12))
entry.pack(side="left", fill="x", expand=True, padx=(0,8))

tk.Button(top, text="Add", width=10, command=add_task).pack(side="left")
tk.Button(top, text="Edit", width=10, command=edit_task).pack(side="left", padx=(8,0))
tk.Button(top, text="Clear", width=10, command=clear_input).pack(side="left", padx=(8,0))

mid = tk.Frame(root)
mid.pack(padx=12, pady=10, fill="both", expand=True)

listbox = tk.Listbox(mid, font=("Segoe UI", 12))
listbox.pack(side="left", fill="both", expand=True)

scroll = tk.Scrollbar(mid, orient="vertical", command=listbox.yview)
scroll.pack(side="right", fill="y")

listbox.config(yscrollcommand=scroll.set)

bottom = tk.Frame(root)
bottom.pack(padx=12, pady=(0,10), fill="x")

search_entry = tk.Entry(bottom, font=("Segoe UI", 11), width=25)
search_entry.pack(side="left")

tk.Button(bottom, text="Search", width=10, command=search).pack(side="left", padx=6)
tk.Button(bottom, text="Show All", width=10, command=show_all).pack(side="left")
tk.Button(bottom, text="Toggle Done", width=12, command=toggle_done).pack(side="right")
tk.Button(bottom, text="Delete", width=10, command=delete_task).pack(side="right", padx=6)

def on_return(e):
    if entry.get().strip():
        add_task()
root.bind("<Return>", on_return)

tasks = load()
refresh()
root.mainloop()