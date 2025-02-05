from pathlib import Path

#Diretorio para armazenar arquivos temporarios
STORAGE_DIR = Path('storage')
STORAGE_DIR.mkdir(exist_ok=True)

#Diretorio para logs 
LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

#tamanho maximo para arquivos de imagem (em mb)
MAX_FILE_SIZE_MB = 5