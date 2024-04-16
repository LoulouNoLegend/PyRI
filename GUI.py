import os
import requests
import zipfile
import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog

# Function to change the message at the bottom left
# You can choose the text, the color and after how many miliseconds it will disappear (exemple: 5000 = 5s)
def success_text(text, color, time):
    success_label.config(text=text, fg=color)
    if time == -1:
        return None
    else:
        root.after(time, lambda: success_label.config(text=""))  # Clear the message after 5 seconds

# It's here that everything is downloading.
def download_latest_release(repo_name, target_dir):
    success_text(f"Downloading from {repo_name}", "black", -1)
    url = f"https://api.github.com/repos/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info.get('assets', [])
        if isZip.get() == True:
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
                        success_text(f"Failed to download the release: {e}", "red", 7000)
                        return None
        else:
            if assets:
                for asset in assets:  # Go trough all assets
                    asset_url = asset.get('browser_download_url')
                    asset_name = asset.get('name')
                    if asset_url:
                        try:
                            # Download with requests
                            with requests.get(asset_url, stream=True) as r:
                                r.raise_for_status()
                                # Save the file in the choosed directory
                                file_path = os.path.join(target_dir, asset_name)
                                with open(file_path, 'wb') as f:
                                    shutil.copyfileobj(r.raw, f)
                                success_text("Latest Release Downloaded!", "green", 7000)
                        except Exception as e:
                            success_text(f"Failed to download the release: {e}", "red", 7000)
                            return None
    else:
        success_text(f"Failed to get release information: {response.text}", "red", 7000)
    return None


# The downloaded zip file is extracted!!!
def extract_zip(zip_data, target_dir):
    with tempfile.TemporaryFile() as tmp:
        tmp.write(zip_data)
        with zipfile.ZipFile(tmp) as zip_file:
            zip_file.extractall(target_dir)

def download_and_extract():
    repo_name = username_entry.get() + "/" + repo_entry.get()
    target_dir = directory_entry.get()
    success_text("Downloading the latest release...", "black", -1)
    
    release_data = download_latest_release(repo_name, target_dir)
    if isZip.get()==True:
        if release_data:
            success_text(f"Extracting the release to: {target_dir}", "black", -1)
            extract_zip(release_data, target_dir)
            
            success_text("Latest Release Downloaded!", "green", 7000)
        else:
            success_text("Download failed.", "red", 7000)
        

def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)
    
def show_info():
    info_window = tk.Toplevel(root)
    info_window.title("Information")
    info_label = tk.Label(info_window, text="Made by LoulouNoLegend")
    info_label.pack()

def checkbutton_clicked():
    print("New state:", isZip.get())

# Create the main window
root = tk.Tk()
root.title("PyRI")
root.minsize(330, 160)
root.maxsize(330, 160)


# A canva so the text doesn't move everything 😭
text_canvas = tk.Canvas(root, width=325, height=20)
text_canvas.grid(row=6, column=0, columnspan=3)


# Entry fields and labels
username_label = tk.Label(root, text="GitHub Username:")
username_entry = tk.Entry(root)

repo_label = tk.Label(root, text="Repository Name:")
repo_entry = tk.Entry(root)

directory_label = tk.Label(root, text="Target Directory:")
directory_entry = tk.Entry(root)

success_label = tk.Label(root, text="", fg="black")

text_label = tk.Label(text_canvas, text="Made by LoulouNoLegend", fg="black")


# The buttons
browse_button = tk.Button(root, text="Browse", command=browse_directory)
download_button = tk.Button(root, text="Download", command=download_and_extract)
#info_button = tk.Button(root, text="i", command=show_info)

# Other things
isZipCheckBox_label = tk.Label(root, text="Is the release a zip?")
isZip = tk.BooleanVar(value=False)
isZipCheckBox = tk.Checkbutton(root, text='', variable=isZip, command=checkbutton_clicked)


# Grid of objects
username_label.grid(row=0, column=0, sticky="W")
username_entry.grid(row=0, column=1, sticky="EW")

repo_label.grid(row=1, column=0, sticky="W")
repo_entry.grid(row=1, column=1, sticky="EW")

directory_label.grid(row=2, column=0, sticky="W")
directory_entry.grid(row=2, column=1, sticky="EW")

browse_button.grid(row=2, column=2, sticky="EW")

isZipCheckBox_label.grid(row=3, column=0, sticky="W")
isZipCheckBox.grid(row=3, column=1, sticky="EW")

download_button.grid(row=4, column=1, sticky="EW")
#info_button.grid(row=0, column=2, sticky="E")

success_label.grid(row=5, column=1, sticky="EW")

text_label.grid(row=6, column=0, sticky="W")
text_canvas.create_window(0, 0, anchor="nw", window=text_label)

# Start the Tkinter event loop
root.mainloop()
