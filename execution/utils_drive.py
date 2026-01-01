import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils_auth import get_credentials

def get_drive_service():
    """Builds Drive API service."""
    creds = get_credentials()
    if not creds:
        print("Auth failed for Drive.")
        return None
    return build('drive', 'v3', credentials=creds)

def get_or_create_folder(folder_name):
    """Finds or creates a folder in the root directory."""
    service = get_drive_service()
    if not service: return None
    
    # Check if folder exists
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    
    if files:
        print(f"Found existing folder '{folder_name}' (ID: {files[0]['id']})")
        return files[0]['id']
    else:
        # Create folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Created new folder '{folder_name}' (ID: {folder['id']})")
        return folder['id']

def upload_file(file_path, folder_id):
    """Uploads a file to the specified Drive folder and returns user-viewable link."""
    service = get_drive_service()
    if not service: return None
    
    file_name = os.path.basename(file_path)
    
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(file_path, resumable=True)
    
    print(f"Uploading '{file_name}' to Drive...")
    file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    
    print(f"Upload Complete. File ID: {file.get('id')}")
    return file.get('webViewLink')

if __name__ == "__main__":
    # Test
    folder_id = get_or_create_folder("Jarvis Test Folder")
    if folder_id:
        print(f"Folder ID: {folder_id}")
