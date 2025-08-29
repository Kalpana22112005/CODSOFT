import tkinter as tk
from tkinter import messagebox

def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

def equalpress():
    global expression
    try:
        result = str(eval(expression))
        equation.set(result)
        expression = result
    except ZeroDivisionError:
        messagebox.showerror("Error", "❌ Division by Zero not allowed!")
        expression = ""
        equation.set("")
    except:
        messagebox.showerror("Error", "❌ Invalid Input!")
        expression = ""
        equation.set("")

def clear():
    global expression
    expression = ""
    equation.set("")

def backspace():
    global expression
    expression = expression[:-1]
    equation.set(expression)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    if dark_mode: 
        root.config(bg="#1e1e1e")
        entry_field.config(bg="#2d2d2d", fg="white", insertbackground="white")
        for b in all_buttons:
            b.config(bg="#333333", fg="white", activebackground="#444444", activeforeground="white")
        eq_btn.config(bg="#4CAF50", fg="white")
        clear_btn.config(bg="#ff4c4c", fg="white")
        back_btn.config(bg="#888888", fg="white")
        theme_btn.config(text="🔆")
    else:
        root.config(bg="white")
        entry_field.config(bg="white", fg="black", insertbackground="black")
        for b in all_buttons:
            b.config(bg="#f0f0f0", fg="black", activebackground="#d9d9d9", activeforeground="black")
        eq_btn.config(bg="#4CAF50", fg="white")
        clear_btn.config(bg="#f44336", fg="white")
        back_btn.config(bg="#cccccc", fg="black")
        theme_btn.config(text="🌙")

root = tk.Tk()
root.title("🧮 Calculator")
root.geometry("360x540")
root.resizable(False, False)

expression = ""
equation = tk.StringVar()

entry_field = tk.Entry(root, textvariable=equation, font=("Segoe UI", 18),
                       justify="right", bd=8, relief="ridge")
entry_field.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=15, pady=10)

theme_btn = tk.Button(root, text="🌙", command=toggle_theme, font=("Segoe UI", 12), bd=0)
theme_btn.place(x=320, y=5)

btn_style = {"font": ("Segoe UI", 14), "bd": 5, "relief": "ridge", "width": 5, "height": 2}

buttons = [
    ("7",1,0), ("8",1,1), ("9",1,2), ("/",1,3),
    ("4",2,0), ("5",2,1), ("6",2,2), ("*",2,3),
    ("1",3,0), ("2",3,1), ("3",3,2), ("-",3,3),
    ("0",4,0), (".",4,1), ("=",4,2), ("+",4,3),
]

all_buttons = []

for (text, row, col) in buttons:
    if text == "=":
        b = tk.Button(root, text=text, command=equalpress, **btn_style)
        eq_btn = b
    else:
        b = tk.Button(root, text=text, command=lambda t=text: press(t), **btn_style)
    b.grid(row=row, column=col, padx=5, pady=5)
    all_buttons.append(b)

clear_btn = tk.Button(root, text="AC", command=clear, **btn_style)
clear_btn.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
all_buttons.append(clear_btn)

back_btn = tk.Button(root, text="⌫", command=backspace, **btn_style)
back_btn.grid(row=5, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)
all_buttons.append(back_btn)

dark_mode = False
apply_theme()

root.mainloop()