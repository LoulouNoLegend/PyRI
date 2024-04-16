#import os
import requests
import zipfile
import tempfile
import tkinter as tk
from tkinter import filedialog

def success_text(text, color, time):
    success_label.config(text=text, fg=color)
    if time == -1:
        return
    else:
        root.after(time, lambda: success_label.config(text=""))  # Clear the message after 5 seconds

def download_latest_release(repo_name):
    success_text("Downloading from " + repo_name, "black", -1)
    url = f"https://api.github.com/repos/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info.get('assets', [])
        if assets:
            asset = assets[0]  # (Assuming the first asset is the zip file... I need to do something about it, fr)
            asset_url = asset.get('browser_download_url')
            if asset_url:
                try:
                    # Download the release file using requests, because I love requests!!!
                    with requests.get(asset_url, stream=True) as r:
                        r.raise_for_status()
                        release_data = r.content
                    return release_data
                except Exception as e:
                    success_text("Failed to download the release: " + e, "red", 5000)
    else:
        success_text("Failed to get release information:" + response.text, "black", -1)
    return None

def extract_zip(zip_data, target_dir):
    with tempfile.TemporaryFile() as tmp:
        tmp.write(zip_data)
        with zipfile.ZipFile(tmp) as zip_file:
            zip_file.extractall(target_dir)

def download_and_extract():
    repo_name = username_entry.get() + "/" + repo_entry.get()
    target_dir = directory_entry.get()
    success_text("Downloading the latest release...", "black", -1)
    
    release_data = download_latest_release(repo_name)
    if release_data:
        success_text("Extracting the release to: " + target_dir, "black", -1)
        extract_zip(release_data, target_dir)
                
        # Display a success message
        success_text("Latest Release Downloaded!", "green", 5000)
    else:
        success_text("Download failed.", "red", 5000)

def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)
    
def show_info():
    info_window = tk.Toplevel(root)
    info_window.title("Information")
    info_label = tk.Label(info_window, text="Made by LoulouNoLegend")
    info_label.pack()



# Create the main window
root = tk.Tk()
root.title("PyRI")
root.minsize(325, 115)
root.maxsize(325, 115)



# Entry fields and labels
username_label = tk.Label(root, text="GitHub Username:")
username_entry = tk.Entry(root)

repo_label = tk.Label(root, text="Repository Name:")
repo_entry = tk.Entry(root)

directory_label = tk.Label(root, text="Target Directory:")
directory_entry = tk.Entry(root)

success_label = tk.Label(root, text="", fg="black")



# The buttons
browse_button = tk.Button(root, text="Browse", command=browse_directory)
download_button = tk.Button(root, text="Download", command=download_and_extract)
#info_button = tk.Button(root, text="i", command=show_info)



# Grid of objects
username_label.grid(row=0, column=0, sticky="W")
username_entry.grid(row=0, column=1, sticky="W")

repo_label.grid(row=1, column=0, sticky="W")
repo_entry.grid(row=1, column=1, sticky="W")

directory_label.grid(row=2, column=0, sticky="W")
directory_entry.grid(row=2, column=1, sticky="W")

browse_button.grid(row=2, column=2, sticky="W")
download_button.grid(row=3, column=1, sticky="W")
#info_button.grid(row=0, column=2, sticky="E")

success_label.grid(row=5, column=0, sticky="W")

# Start the Tkinter event loop
root.mainloop()
