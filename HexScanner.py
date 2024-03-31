'''Hex Scanner by VincentNL 31/03/2024'''

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import shutil
import mmap

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def search_bytes_in_folder(target_folder, target_bytes):
    results = []
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        if mm.find(target_bytes) != -1:
                            results.append(file_path)
            except (OSError, IOError):
                pass
    return results

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        result_listbox.delete(0, tk.END)  # Clear any previous results
        target_bytes = bytes.fromhex(byte_entry.get("1.0", tk.END).strip())
        files_with_target_bytes = search_bytes_in_folder(folder_path, target_bytes)
        if files_with_target_bytes:  # Display results only if at least one item is found
            for file_path in files_with_target_bytes:
                result_listbox.insert(tk.END, file_path)
            root.geometry(size_full)
            result_listbox.pack(pady=0)
            save_button.pack(pady=30)

            # Adjust the window geometry upon search if needed
            root.geometry(size_full)
        else:
            # Adjust the window geometry if no results found
            root.geometry(size_half)

def save_log():
    log_content = result_listbox.get(0, tk.END)
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if save_path:
        log_dir, log_filename = os.path.split(save_path)
        log_folder = os.path.join(log_dir, os.path.splitext(log_filename)[0])
        os.makedirs(log_folder, exist_ok=True)
        with open(save_path, 'w') as f:
            f.write("\n".join(log_content))

def copy_to_clipboard():
    selected_item = result_listbox.get(result_listbox.curselection())
    root.clipboard_clear()
    root.clipboard_append(selected_item)
    root.update()

def open_folder_and_select_file():
    selected_item = result_listbox.get(result_listbox.curselection())
    os.system(f'explorer /select,"{os.path.normpath(selected_item)}"')

def open_with_hxd():
    selected_item = result_listbox.get(result_listbox.curselection())
    hxd_path = r'C:/Program Files/HxD/HxD.exe'
    cmd = fr'"{hxd_path}" "{selected_item}"'
    subprocess.Popen(cmd, shell=True)

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# Create main window
root = tk.Tk()
root.title("Hex Scanner")

size_half = "640x196"
size_full = "640x440"
root.geometry(size_half)  # Initial size
root.resizable(False, False)
root.iconbitmap(resource_path('naomi9.ico'))

# Create widgets
tk.Label(root, text="Enter bytes (hex):").pack(pady=10)

byte_entry = tk.Text(root, width=60, height=2, wrap=tk.WORD)
byte_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse & Scan!", command=browse_folder)
browse_button.pack(pady=40)

result_listbox = tk.Listbox(root, width=100)
save_button = tk.Button(root, text="Save Log", command=save_log)

# Create context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Open with HxD", command=open_with_hxd)
context_menu.add_command(label="Open Folder", command=open_folder_and_select_file)
context_menu.add_command(label="Copy path", command=copy_to_clipboard)

# Bind events
result_listbox.bind("<Button-3>", show_context_menu)
root.mainloop()