import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

# Note: All button text colors should always be black for visibility.

def download_video():
    url = url_var.get()
    platform = platform_var.get()
    output_folder = output_var.get() or 'downloads'
    filename = filename_var.get()
    
    if not url.strip():
        messagebox.showwarning("Input Error", "Please enter a valid URL")
        return
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    status_label.config(text="Initializing Download...")
    root.update_idletasks()
    
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, filename if filename else '%(title)s.%(ext)s'),
        'progress_hooks': [update_status]
    }
    
    try:
        status_label.config(text="Fetching Video Information...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            default_filename = ydl.prepare_filename(info_dict)
            filename_var.set(default_filename)
            ydl.download([url])
        status_label.config(text=f"Download Complete! Saved to: {os.path.join(output_folder, filename)}")
        messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        status_label.config(text=f"Download Failed: {e}")
        messagebox.showerror("Error", f"Error downloading video: {e}")

def update_status(d):
    if d['status'] == 'downloading':
        status_label.config(text=f"Downloading: {d['_percent_str']} - {d['_eta_str']} remaining")
    elif d['status'] == 'finished':
        status_label.config(text="Download Complete!")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_var.set(folder_selected)

def update_filename():
    url = url_var.get()
    if not url.strip():
        return
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            filename_var.set(ydl.prepare_filename(info_dict))
    except Exception:
        filename_var.set("")

def clear_fields():
    platform_var.set("X")
    url_var.set("")
    output_var.set("")
    filename_var.set("")
    status_label.config(text="Ready")

# UI Setup
root = tk.Tk()
root.title("Video Downloader")
root.geometry("500x400")
root.configure(bg="#f0f0f0")

platform_var = tk.StringVar(value="X")
url_var = tk.StringVar()
output_var = tk.StringVar()
filename_var = tk.StringVar()

tk.Label(root, text="Select Platform:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
platform_dropdown = ttk.OptionMenu(root, platform_var, "X", "X", "LinkedIn")
platform_dropdown.pack()

tk.Label(root, text="Enter Video URL:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
tk.Entry(root, textvariable=url_var, width=60, font=("Arial", 10)).pack(pady=5)

tk.Label(root, text="Select Output Folder:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack()
tk.Entry(frame, textvariable=output_var, width=40, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Browse", command=browse_folder, font=("Arial", 10), bg="#4CAF50", fg="black").pack(side=tk.LEFT)

tk.Label(root, text="Filename:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
tk.Entry(root, textvariable=filename_var, width=60, font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="Fetch Filename", command=update_filename, font=("Arial", 10), bg="#FFA500", fg="black").pack()

tk.Button(root, text="Download Video", command=download_video, font=("Arial", 12, "bold"), bg="#008CBA", fg="black", padx=15, pady=7).pack(pady=10)
tk.Button(root, text="Clear", command=clear_fields, font=("Arial", 12), bg="#f44336", fg="black", padx=15, pady=7).pack(pady=5)

status_label = tk.Label(root, text="Ready", bg="#f0f0f0", font=("Arial", 10))
status_label.pack(pady=5)

root.mainloop()

