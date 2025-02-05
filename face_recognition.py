import cv2
import dlib
import numpy as np

# Carregar os modelos do Dlib
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

def extract_embeddings(image):
    """
    Extrai os embeddings faciais da imagem.
    """
    try:
        if image is None:
            return np.array([])
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converter para escala de cinza
        faces = detector(gray)  # Detectar rosto

        if len(faces) == 0:
            return np.array([])  # Nenhum rosto detectado
        
        for face in faces:
            shape = shape_predictor(gray, face)
            embedding = face_rec_model.compute_face_descriptor(image, shape)
            return np.array(embedding) / np.linalg.norm(embedding)  # Normalizar vetor
        
        return np.array([])  # Caso nenhum rosto seja processado
    except Exception as e:
        return np.array([])  # Retorna vazio em caso de erro
