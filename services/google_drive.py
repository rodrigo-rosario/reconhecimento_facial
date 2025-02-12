import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()  # Carregar variáveis do .env

# Configuração da API do Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDENTIALS_PATH")
MAIN_FOLDER_ID = os.getenv("MAIN_FOLDER_ID")

# Conectar ao Google Drive
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Função para obter o ID de uma pasta pelo nome dentro de um diretório
def get_folder_id(name, parent_id):
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parent_id}' in parents"
    
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get('files', [])
    
    return folders[0]['id'] if folders else None

# Função para listar todas as imagens dentro de uma pasta
def list_images_in_folder(folder_id):
    query = f"mimeType contains 'image/' and trashed=false and '{folder_id}' in parents"
    
    results = service.files().list(q=query, fields="files(id, name, webContentLink)").execute()
    return results.get('files', [])
