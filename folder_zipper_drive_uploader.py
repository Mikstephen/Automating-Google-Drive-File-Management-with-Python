from google.colab import drive
drive.mount('/content/drive')
import os
import shutil
import time
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Authenticate Google Drive API
auth.authenticate_user()
creds, _ = auth.default()
drive_service = build('drive', 'v3', credentials=creds)

# Step 1: Set Parent Directory Dynamically
parent_dir = input("Enter the Google Drive path (Example: /content/drive/My Drive/Sunset Digital Labs/2024/Products/Clip Art/ ").strip()
parent_folder_name = os.path.basename(parent_dir)

# Define log_file_path before using it in log_message
output_dir = os.path.join(parent_dir, "zipped_folders")
os.makedirs(output_dir, exist_ok=True)
log_file_path = os.path.join(output_dir, f"{parent_folder_name}_log.txt")

def log_message(message):
    """Save logs to a text file and print them."""
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

def folder_exists(folder_path):
    """Check if the given folder path exists."""
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        log_message(f"✅ The specified folder '{folder_path}' exists.")
        return True
    else:
        log_message(f"❌ Error: The specified folder '{folder_path}' does not exist. Please check the path and try again.")
        return False

if folder_exists(parent_dir):
    log_message("\n🚀 Starting Folder Zipping Process...\n")

    # Step 2: List all subdirectories
    subfolders = [f for f in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, f)) and f != "zipped_folders"]
    folder_count = len(subfolders)

    log_message(f"🔍 Found {folder_count} folders: {subfolders}\n")

    # Step 3: Zip each subfolder
    zipped_files = []
    for folder in subfolders:
        folder_path = os.path.join(parent_dir, folder)
        zip_path = os.path.join(output_dir, folder)  # No .zip extension needed

        shutil.make_archive(zip_path, 'zip', folder_path)  # Fast zipping
        zip_file = f"{zip_path}.zip"
        zipped_files.append(zip_file)

        log_message(f"✅ Zipped {folder} -> {zip_file}")

    log_message("\n🎉 All folders zipped successfully!\n")

    # Step 4: Upload each ZIP file to Google Drive and get a direct download link
    def upload_to_drive(file_path):
        file_name = os.path.basename(file_path)
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, mimetype='application/zip')

        try:
            uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Make the file publicly accessible
            drive_service.permissions().create(
                fileId=uploaded_file['id'],
                body={'role': 'reader', 'type': 'anyone'},
            ).execute()

            # Generate direct download link
            file_id = uploaded_file['id']
            file_link = f"https://drive.google.com/uc?export=download&id={file_id}"

            return file_link  # Return direct download link

        except HttpError as e:
            log_message(f"❌ Error uploading {file_name}: {e}")
            return None

    # Step 5: Upload and Generate Public Links
    download_links = {}
    for zip_file in zipped_files:
        time.sleep(1)  # Add delay to avoid hitting API quotas
        link = upload_to_drive(zip_file)
        if link:
            download_links[os.path.basename(zip_file)] = link
            log_message(f"📤 Uploaded {zip_file} -> 🔗 {link}")

    log_message("\n🎉 All zip files uploaded successfully!\n")

    # Display final links
    log_message("\n🔗 Direct Download Links:")
    for file_name, link in download_links.items():
        log_message(f"📂 {file_name}: {link}")

    log_message("\n✅ Process Completed. Log saved to " + log_file_path)