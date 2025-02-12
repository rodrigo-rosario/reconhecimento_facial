from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import cv2
import numpy as np
from services.face_recognition import extract_embeddings
from services.google_drive import get_folder_id, list_images_in_folder, MAIN_FOLDER_ID
import requests

app = FastAPI()

@app.post("/upload-selfie/")
async def upload_selfie(file: UploadFile = File(...), event: str = "Casamento", month_year: str = "02-2025"):
    """
    Recebe a selfie, identifica a pasta no Google Drive e busca as imagens correspondentes para comparação.
    """
    try:
        # Salvar temporariamente a selfie
        temp_path = f"storage/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Carregar imagem e extrair embeddings
        image = cv2.imread(temp_path)
        selfie_embeddings = extract_embeddings(image)

        if selfie_embeddings.size == 0:
            raise HTTPException(status_code=400, detail="Nenhum rosto detectado na selfie.")

        # Buscar a pasta correta no Google Drive
        category_id = get_folder_id(event, MAIN_FOLDER_ID)
        if not category_id:
            return {"error": f"Categoria '{event}' não encontrada."}

        folder_id = get_folder_id(f"{event} {month_year}", category_id)
        if not folder_id:
            return {"error": f"Nenhuma subpasta encontrada para '{event} {month_year}'."}

        # Listar imagens da pasta
        images = list_images_in_folder(folder_id)
        if not images:
            return {"error": f"Nenhuma imagem encontrada na pasta '{event} {month_year}'."}

        # Comparar selfies com imagens do Drive
        matched_images = []
        for img in images:
            img_url = img["webContentLink"]
            
            # Baixar a imagem do Google Drive
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_array = np.asarray(bytearray(img_response.content), dtype=np.uint8)
                img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                # Extrair embeddings e comparar
                img_embeddings = extract_embeddings(img_cv)
                if img_embeddings.size > 0:
                    similarity = np.dot(selfie_embeddings, img_embeddings)  # Similaridade por produto interno
                    if similarity > 0.6:  # Limiar de similaridade
                        matched_images.append(img_url)

        return {"message": "Selfie processada com sucesso", "matched_images": matched_images}

    except Exception as e:
        return {"error": str(e)}
