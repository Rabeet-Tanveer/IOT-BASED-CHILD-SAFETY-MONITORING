import os
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build


# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "baby-monitoring-423103-df71c8182603.json"

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

def create_folder(folder_name, parent_folder_id=None):
    """Create a folder in Google Drive and return its ID."""
    folder_metadata = {
        'name': folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        'parents': [parent_folder_id] if parent_folder_id else []
    }

    created_folder = drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()

    print(f'Created Folder ID: {created_folder["id"]}')
    return created_folder["id"]

def upload_file(file_path, folder_id=None):
    """Upload a file to Google Drive."""
    file_metadata = {'name': os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path)

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f'Uploaded File ID: {uploaded_file["id"]}')
    return uploaded_file["id"]

def list_folder(parent_folder_id=None, delete=False):
    """List folders and files in Google Drive."""
    results = drive_service.files().list(
        q=f"'{parent_folder_id}' in parents and trashed=false" if parent_folder_id else None,
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])

    if not items:
        print("No folders or files found in Google Drive.")
    else:
        print("Folders and files in Google Drive:")
        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")
            if delete:
                delete_files(item['id'])

def delete_files(file_or_folder_id):
    """Delete a file or folder in Google Drive by ID."""
    try:
        drive_service.files().delete(fileId=file_or_folder_id).execute()
        print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
    except Exception as e:
        print(f"Error deleting file/folder with ID: {file_or_folder_id}")
        print(f"Error details: {str(e)}")

def download_file(file_id, destination_path):
    """Download a file from Google Drive by its ID."""
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, mode='wb')
    
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
        
        
def upload_and_replace_file(file_path, folder_id=None):
    """Upload a file to Google Drive, replacing an existing file if it already exists."""
    file_name = os.path.basename(file_path)
    existing_file_id = get_file_id_by_name(file_name, folder_id)
    
    if existing_file_id:
        # If file already exists, delete it first
        delete_files(existing_file_id)
    
    # Upload the new file
    return upload_file(file_path, folder_id)

def get_file_id_by_name(file_name, folder_id=None):
    """Get the ID of a file in Google Drive by its name."""
    query = f"name='{file_name}'"
    if folder_id:
        query += f" and '{folder_id}' in parents"
    
    results = drive_service.files().list(
        q=query,
        pageSize=1,
        fields="files(id)"
    ).execute()
    
    files = results.get('files', [])
    if files:
        return files[0]['id']
    else:
        return None

def download_file_by_name(file_name, destination_path, folder_id=None):
    """Download a file from Google Drive by its name."""
    file_id = get_file_id_by_name(file_name, folder_id)
    
    if file_id:
        download_file(file_id, destination_path)
        print(f"Downloaded file '{file_name}' successfully to '{destination_path}'")
    else:
        print(f"File '{file_name}' not found in Google Drive.")
        

if __name__ == '__main__':
#    create_folder("MyNewFolder")
    
    file_path_to_upload = "frame.jpg"
    upload_and_replace_file(file_path_to_upload)
    # Delete a file or folder by ID
    # delete_files("1XFkFWuL7ThPco-OGEVAtq-7RxCCMikxR")


    
    # Upload a file to Google Drive
    #file_path_to_upload = "frame.jpg"
    # folder_id_to_upload = "1UbudMVbgF_73uvFz-7v6OMAD7nkAL4H_"  # Optional, specify the folder ID if you want to upload the file into a specific folder
    #upload_file(file_path_to_upload)

    
    list_folder()
    # Download a file by its ID
    #download_file("1OAvQrK2ZCnLf7yJxeJLkoZg7nHXnXVHm", "file_name.avi")
