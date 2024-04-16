import os
import requests
import zipfile
import shutil
import tempfile

# This thing is like a function to.. download the latest release. Omg it's so cool, I know!
def download_latest_release(repo_name, target_dir, isZip):
    url = f"https://api.github.com/repos/{repo_name}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info.get('assets', [])
        if isZip == True:
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
                        print(f"Failed to download the release: {e}")
                        return None
        else:
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
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
                                print("Latest Release Downloaded!")
                        except Exception as e:
                            print(f"Failed to download the release: {e}")
                            return None
    else:
        print(f"Failed to get release information: {response.text}")
    return None

def extract_zip(zip_data, target_dir):
    with tempfile.TemporaryFile() as tmp:
        tmp.write(zip_data)
        with zipfile.ZipFile(tmp) as zip_file:
            zip_file.extractall(target_dir)

def main():
    # Ask for user input
    repo_name = input("Enter the name of the GitHub repository (format: username/repo): ")
    isZipInput = input("Is the release a single zip file (y/n): ")
    target_dir = input("Enter the directory where you want to install the release (format: disk:/folder/folder... ): ")
    
    if isZipInput == "y":
        isZip = True
    else:
        isZip = False

    # Check if the target directory exists
    if not os.path.exists(target_dir):
        print("Downloading the latest release...")
        release_data = download_latest_release(repo_name, target_dir, isZip)
        if isZip == True:
            if release_data:
                print(f"Extracting the release to: {target_dir}")
                extract_zip(release_data, target_dir)

                print("Installation completed!")
            else:
                # Even more skill issue, you were about to finish all this, but no
                print("Failed to download the latest release.")
    else:
        directoryExists = input("The directory already exists. Do you still want to continue and overwrite the files? (y/n): ")
        if directoryExists == "n":
            exit
        else:
            release_data = download_latest_release(repo_name, target_dir, isZip)
            if isZip == True:
                if release_data:
                    extract_zip(release_data, target_dir)
                    print("Files were overwritten.")

if __name__ == "__main__":
    main()
