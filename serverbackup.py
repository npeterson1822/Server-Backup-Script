import os
import shutil
from datetime import datetime, timedelta
import subprocess
import getpass


UNC_PATH = r"\\SOURCE PATH GOES HERE"
PREFIX = "prefix"
DEST_ROOT = r"DEST PATH GOES HERE"
USERNAME = "username"

# Auth into specified server drive
def prompt_network_auth(unc_path, username):
    print(f"Authenticating to {unc_path} as {username}...")
    password = getpass.getpass(prompt="Enter admin password: ")

    #Net use to map drive and connect with creds
    result = subprocess.run(
        ["net", "use", unc_path, f"/user:{username}", password],
        capture_output=True,
        text=True
    )
    #Non-zero return code indicates failure
    if result.returncode != 0:
        print(f"Failed to authenticate:\n{result.stderr}")
        exit(1)
    else:
        print("Authentication successful.")


def main():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    #Use set prefix & date to determine which folders to copy/keep
    folder_today = f"{PREFIX}({today.strftime('%m-%d-%Y')})"
    folder_yesterday = f"{PREFIX}({yesterday.strftime('%m-%d-%Y')})"

    dest_path = os.path.join(DEST_ROOT, folder_today)


    # Test access and create "folders" list, ensuring it's all dirs
    try:
        folders = [f for f in os.listdir(UNC_PATH) if os.path.isdir(os.path.join(UNC_PATH, f))]
    except PermissionError:
        print("Access denied. Make sure you're authenticated to the server.")
        return

    # Check if today's folder is in the list, if so, copy it to destination with robocopy.
    if folder_today in folders:
        src_folder = os.path.join(UNC_PATH, folder_today)
        print(f"Copying {src_folder} to {dest_path} (this may take a while)...")

    # robocopy command arguments
        robocopy_cmd = [
            "robocopy",
            src_folder,
            dest_path,
            "/MIR",     # Deletes files in dest that aren't mirrored in src (never should apply)
            "/Z",       # Support resuming with crashes
            "/MT:16",   # 16 threads
            "/R:10",    # Retry 10 times on failure
            "/W:5"      # Wait 5 seconds between retries
        ]

    # Run robocopy
        result = subprocess.run(robocopy_cmd, capture_output=True, text=True)

        if result.returncode >= 8:
            print(f"Robocopy failed with code {result.returncode}. See output:\n{result.stdout}")
            return
        else:
            print("Copy completed successfully.")
    else:
        print(f"Today's folder not found: {folder_today}")
        return

    # Shututil rmtree deleting any folder in folders list that isn't today or yesterday
    for folder in folders:
        if folder.startswith(PREFIX) and folder not in (folder_today, folder_yesterday):
            full_path = os.path.join(UNC_PATH, folder)
            try:
                print(f"Deleting {full_path}")
                shutil.rmtree(full_path)
            except Exception as e:
                print(f"Error deleting {folder}: {e}")



if __name__ == "__main__":
    prompt_network_auth(UNC_PATH, USERNAME)
    main()
    