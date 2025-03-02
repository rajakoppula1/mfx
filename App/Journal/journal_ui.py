import tkinter as tk
from tkinter import ttk
import datetime
import os
import subprocess

# File path for journal entries
JOURNAL_FILE = "journal.txt"

# Task status options
TASK_STATUSES = [
    "Not reviewed", "Not a task", "Not started",
    "Planning", "Execution", "Completed", "Hold"
]

# Function to read and parse journal entries
def load_entries():
    try:
        with open(JOURNAL_FILE, "r") as file:
            entries = []
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(" - ")
                    if len(parts) == 3:
                        timestamp, text, status = parts
                    else:
                        timestamp, text = parts[0], parts[1]
                        status = "Not reviewed"
                    entries.append((timestamp, text, status))
            return entries
    except FileNotFoundError:
        return []

# Function to get project start info
def get_project_start_info(entries):
    if not entries:
        return "N/A", "N/A"
    
    first_entry = entries[0][0]
    start_date = datetime.datetime.strptime(first_entry, "%Y-%m-%d %H:%M:%S").date()
    days_elapsed = (datetime.date.today() - start_date).days
    return start_date, days_elapsed

# Function to save updated entries
def save_entries(entries):
    with open(JOURNAL_FILE, "w") as file:
        for timestamp, text, status in entries:
            file.write(f"{timestamp} - {text} - {status}\n")
    auto_push_to_github()

# Function to auto-push to GitHub
def auto_push_to_github():
    try:
        subprocess.run(["git", "add", JOURNAL_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Updated journal entries"], check=True)
        subprocess.run(["git", "push"], check=True)
    except subprocess.CalledProcessError:
        print("Git push failed. Ensure your repository is set up correctly.")

# Function to update task status of an entry
def update_status(index, status_var):
    new_status = status_var.get()
    timestamp, text, _ = all_entries[index]
    all_entries[index] = (timestamp, text, new_status)

    save_entries(all_entries)
    update_listbox(all_entries)

# Function to apply filters
def apply_filters():
    selected_status = status_filter.get()
    search_text = search_entry.get().strip().lower()

    filtered_entries = [
        (timestamp, text, status) for timestamp, text, status in all_entries
        if (selected_status == "All" or status == selected_status)
        and (not search_text or search_text in text.lower())
    ]
    
    update_listbox(filtered_entries)

# Function to update the UI listbox with journal entries
def update_listbox(entries):
    for widget in entries_frame.winfo_children():
        widget.destroy()

    for index, (timestamp, text, status) in enumerate(entries):
        entry_frame = tk.Frame(entries_frame)
        entry_frame.pack(fill="x", padx=5, pady=2)

        entry_label = tk.Label(entry_frame, text=f"{timestamp} - {text}", anchor="w", width=60)
        entry_label.pack(side="left", padx=5)

        status_var = tk.StringVar(value=status)
        status_dropdown = ttk.Combobox(entry_frame, textvariable=status_var, values=TASK_STATUSES, width=12)
        status_dropdown.pack(side="left", padx=5)

        save_button = tk.Button(entry_frame, text="Save", command=lambda i=index, sv=status_var: update_status(i, sv))
        save_button.pack(side="left", padx=5)

# Load journal entries
all_entries = load_entries()
project_start_date, days_elapsed = get_project_start_info(all_entries)

# Create main window
root = tk.Tk()
root.title("Journal Viewer")
root.geometry("800x600")

# Title
title_label = tk.Label(root, text="Journal Viewer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Display project start date and days elapsed
start_date_label = tk.Label(root, text=f"Project Start Date: {project_start_date}", font=("Arial", 10))
start_date_label.pack(pady=5)

days_elapsed_label = tk.Label(root, text=f"Days Elapsed: {days_elapsed}", font=("Arial", 10))
days_elapsed_label.pack(pady=5)

# Filter section (aligned compactly)
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

status_filter = ttk.Combobox(filter_frame, values=["All"] + TASK_STATUSES)
status_filter.set("All")
status_filter.pack(side="left", padx=2)

search_entry = tk.Entry(filter_frame, width=20)
search_entry.pack(side="left", padx=2)

filter_button = tk.Button(filter_frame, text="Apply Filters", command=apply_filters)
filter_button.pack(side="left", padx=2)

# Entries list frame
entries_frame = tk.Frame(root)
entries_frame.pack(pady=10, padx=20, fill="both", expand=True)

update_listbox(all_entries)

# Run the app
root.mainloop()
