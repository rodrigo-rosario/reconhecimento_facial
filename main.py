from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import cv2
import numpy as np
from services.face_recognition import extract_embeddings
from services.image_processing import validate_image
from config import STORAGE_DIR, MAX_FILE_SIZE_MB
import logging

app = FastAPI()

# Configuração de logging
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.post("/upload-selfie")
async def upload_selfie(file: UploadFile = File(...)):
    """
    Endpoint para upload de selfie, validação e extração de embeddings.
    """
    try:
        # Verificar tipo de arquivo
        if not file.content_type.startswith("image/"):
            logging.warning(f"Arquivo inválido: {file.filename}")
            raise HTTPException(status_code=400, detail="Apenas arquivos de imagem são permitidos.")
        
        # Verificar tamanho do arquivo
        file_size_mb = len(file.file.read()) / (1024 * 1024)
        file.file.seek(0)  # Resetar leitura do arquivo
        if file_size_mb > MAX_FILE_SIZE_MB:
            logging.warning(f"Arquivo muito grande: {file.filename} ({file_size_mb:.2f}MB)")
            raise HTTPException(status_code=400, detail=f"O arquivo não pode exceder {MAX_FILE_SIZE_MB}MB.")
        
        # Caminho temporário para armazenar a imagem
        temp_path = STORAGE_DIR / file.filename
        
        # Salvando a imagem
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validar imagem
        image = cv2.imread(str(temp_path))
        if not validate_image(image):
            raise HTTPException(status_code=400, detail="Imagem inválida ou corrompida.")
        
        # Extraindo os embeddings faciais
        embeddings = extract_embeddings(image)
        if embeddings.size == 0:
            raise HTTPException(status_code=400, detail="Nenhum rosto detectado na imagem.")
        
        logging.info(f"Selfie processada com sucesso: {file.filename}")
        return {"message": "Selfie processada com sucesso", "embeddings": embeddings.tolist()}

    except Exception as e:
        logging.error(f"Erro ao processar imagem: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a imagem.")
