import tkinter as tk
import datetime

# File path for journal entries
JOURNAL_FILE = "journal.txt"

# Function to read and process journal entries
def load_entries():
    try:
        with open(JOURNAL_FILE, "r") as file:
            lines = file.readlines()
            entries = [line.strip() for line in lines if line.strip()]
            return entries
    except FileNotFoundError:
        return ["No journal entries found."]

# Function to get project start date and days elapsed
def get_project_start_info(entries):
    if not entries or entries[0] == "No journal entries found.":
        return "N/A", "N/A"
    
    first_entry = entries[0].split(" - ")[0]  # Extract date from first entry
    start_date = datetime.datetime.strptime(first_entry, "%Y-%m-%d %H:%M:%S").date()
    days_elapsed = (datetime.date.today() - start_date).days
    return start_date, days_elapsed

# Load journal entries
entries = load_entries()
project_start_date, days_elapsed = get_project_start_info(entries)

# Create main window
root = tk.Tk()
root.title("Journal Viewer")
root.geometry("500x500")

# Title
title_label = tk.Label(root, text="Journal Viewer", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Subtitle
subtitle_label = tk.Label(root, text="Journal Entries", font=("Arial", 12))
subtitle_label.pack(pady=5)

# Display project start date and days elapsed
start_date_label = tk.Label(root, text=f"Project Start Date: {project_start_date}", font=("Arial", 10))
start_date_label.pack(pady=5)

days_elapsed_label = tk.Label(root, text=f"Days Elapsed: {days_elapsed}", font=("Arial", 10))
days_elapsed_label.pack(pady=5)

# Create frame to hold journal entries
entries_frame = tk.Frame(root)
entries_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Scrollable list of journal entries
entries_listbox = tk.Listbox(entries_frame, width=60, height=15)
entries_listbox.pack(side="left", fill="both", expand=True)

# Scrollbar for the listbox
scrollbar = tk.Scrollbar(entries_frame)
scrollbar.pack(side="right", fill="y")
entries_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=entries_listbox.yview)

# Insert journal entries into the listbox
for entry in entries:
    entries_listbox.insert("end", entry)

# Start the Tkinter event loop
root.mainloop()
