import os
import cv2
import dlib
import numpy as np
import logging
from scipy.spatial import distance

logging.basicConfig(level=logging.INFO)

# Definir caminhos para os modelos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
shape_predictor_path = os.path.join(BASE_DIR, "shape_predictor_68_face_landmarks.dat")
face_rec_model_path = os.path.join(BASE_DIR, "dlib_face_recognition_resnet_model_v1.dat")

# Carregar modelos do Dlib
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(shape_predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

def extract_embeddings(image):
    """ Extrai embeddings faciais de uma imagem """
    try:
        if image is None:
            return np.array([])

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) == 0:
            return np.array([])

        for face in faces:
            shape = shape_predictor(gray, face)
            embedding = face_rec_model.compute_face_descriptor(image, shape)
            return np.array(embedding) / np.linalg.norm(embedding)

        return np.array([])

    except Exception as e:
        print(f"Erro ao extrair embeddings: {e}")
        return np.array([])




def compare_embeddings(embedding1, embedding2, threshold=0.6):
    try:
        if embedding1.size == 0 or embedding2.size == 0:
            logging.warning("Um dos embeddings está vazio!")
            return False

        similarity = distance.euclidean(embedding1, embedding2)
        return similarity < threshold
    except Exception as e:
        logging.error(f"Erro na comparação de embeddings: {e}")
        return False
