import tkinter as tk
import random
import string

def generate_password():
    """Generate a new password using the provided length and optional name."""
    try:
        user_name = name_entry.get().strip()
        length_text = length_entry.get().strip()
        length = int(length_text)

        if length < 6:
            result_label.config(text="⚠️ Password length must be at least 6.")
            hide_action_buttons()
            return

        chars = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(chars) for _ in range(length))

        if user_name:
            result_label.config(
                text=f"👤 User: {user_name}\n\n🔑 Generated Password:\n{password}"
            )
        else:
            result_label.config(text=f"🔑 Generated Password:\n{password}")

        show_action_buttons()

    except ValueError:
        result_label.config(text="⚠️ Please enter a valid number for length.")
        hide_action_buttons()

def copy_to_clipboard():
    """Copy the generated password (last line of result label) to clipboard."""
    text = result_label.cget("text").split("\n")
    if text:
        pwd = text[-1].strip()
        if pwd and "Password" not in pwd and "Please" not in pwd and "length" not in pwd:
            root.clipboard_clear()
            root.clipboard_append(pwd)
            root.update()
            result_label.config(text=f"✅ Password copied!\n{pwd}")
        else:
            result_label.config(text="⚠️ No password to copy yet.")
    else:
        result_label.config(text="⚠️ No password to copy yet.")

def reset_for_new():
    """Clear inputs and result to start fresh."""
    name_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)
    result_label.config(text="✨ Enter details and click Generate.")
    hide_action_buttons()
    name_entry.focus_set()

def show_action_buttons():
    if not copy_button.winfo_ismapped():
        copy_button.pack(pady=4)
    if not generate_again_button.winfo_ismapped():
        generate_again_button.pack(pady=4)

def hide_action_buttons():
    if copy_button.winfo_ismapped():
        copy_button.pack_forget()
    if generate_again_button.winfo_ismapped():
        generate_again_button.pack_forget()

root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("440x380")
root.config(bg="#f0f0f0")

title_label = tk.Label(root, text="🔐 Password Generator",
                       font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

name_label = tk.Label(root, text="👤 Enter your name (optional):",
                      font=("Arial", 12), bg="#f0f0f0")
name_label.pack()
name_entry = tk.Entry(root, font=("Arial", 12), justify="center")
name_entry.pack(pady=5)

length_label = tk.Label(root, text="🔢 Enter password length (min 6):",
                        font=("Arial", 12), bg="#f0f0f0")
length_label.pack()
length_entry = tk.Entry(root, font=("Arial", 12), justify="center")
length_entry.pack(pady=5)

generate_button = tk.Button(root, text="✨ Generate Password",
                            font=("Arial", 12, "bold"),
                            bg="#4CAF50", fg="white",
                            command=generate_password)
generate_button.pack(pady=10)

result_label = tk.Label(root, text="✨ Enter details and click Generate.",
                        font=("Arial", 12), bg="#f0f0f0",
                        fg="blue", wraplength=380, justify="center")
result_label.pack(pady=10)

copy_button = tk.Button(root, text="📋 Copy to Clipboard",
                        font=("Arial", 12, "bold"),
                        bg="#2196F3", fg="white",
                        command=copy_to_clipboard)
generate_again_button = tk.Button(root, text="🔄 Generate Again",
                                  font=("Arial", 12, "bold"),
                                  bg="#FF9800", fg="white",
                                  command=reset_for_new)

hide_action_buttons()
name_entry.focus_set()

root.mainloop()