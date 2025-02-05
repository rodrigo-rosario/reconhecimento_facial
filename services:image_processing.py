import cv2 
def validate_image(image):
    '''
    Valida se a imagem carregada e  valida e possui conteudo

    '''
    if image is None or image.shape[0] == 0 or image.shape[1] == 0:
        return False
    return True