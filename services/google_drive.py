import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()  # Carrega variáveis do .env

# Configuração do Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDENTIALS_PATH")
MAIN_FOLDER_ID = os.getenv("MAIN_FOLDER_ID")

# Conectar ao Google Drive
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

def get_folder_id(name, parent_id):
    """ Retorna o ID de uma pasta pelo nome dentro do Google Drive """
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    return folders[0]['id'] if folders else None

def list_images_in_folder(folder_id):
    """ Lista todas as imagens dentro de uma pasta no Google Drive """
    query = f"mimeType contains 'image/' and trashed=false and '{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name, webContentLink)").execute()
    return results.get('files', [])


def list_folders():
    try:
        results = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()
        return results.get("files", [])
    except Exception as e:
        logging.error(f"Erro ao listar pastas do Google Drive: {e}")
        return []
