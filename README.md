# Google Drive Folder Zipper & Uploader

A Python script that automatically zips subfolders in Google Drive and uploads them back with public download links.

## Features

- 📁 Automatically finds and zips all subfolders in a specified directory
- ☁️ Uploads ZIP files to Google Drive with public access
- 🔗 Generates direct download links for each ZIP file
- 📝 Creates detailed logs of the entire process
- ⚡ Built for Google Colab environment

## Usage

1. Run in Google Colab
2. Enter the path to your Google Drive folder when prompted
3. The script will:
   - Create a `zipped_folders` directory
   - Zip each subfolder
   - Upload to Google Drive
   - Generate public download links
   - Save a log file with all details

## Requirements

- Google Colab environment
- Google Drive API access
- See `requirements.txt` for Python dependencies

## Example

```
Enter path: /content/drive/My Drive/Projects/
✅ Found 3 folders: ['folder1', 'folder2', 'folder3']
✅ All folders zipped and uploaded successfully!
```

## Note

This script is designed specifically for Google Colab and requires Google Drive authentication.