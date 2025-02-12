import os
from pathlib import Path
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Definir caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Diretório para armazenar arquivos temporários
STORAGE_DIR = BASE_DIR / "storage"
LOG_DIR = BASE_DIR / "logs"

# Criar diretórios se não existirem
try:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.info("Diretórios de armazenamento e logs configurados corretamente.")
except Exception as e:
    logging.error(f"Erro ao criar diretórios: {e}")

# Tamanho máximo para arquivos de imagem (em MB)
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convertendo para bytes
