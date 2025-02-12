import faiss
import numpy as np

# Criar índice de busca
index = faiss.IndexFlatL2(128)  # 128 dimensões (mesmo tamanho dos embeddings)

# Mapeamento: ID da imagem -> vetor de embedding
image_map = {}

def add_embedding(image_id, embedding):
    embedding = np.array(embedding).astype("float32").reshape(1, -1)
    index.add(embedding)
    image_map[index.ntotal - 1] = image_id  # Associa ID ao índice FAISS

def search_similar(embedding, top_k=5):
    embedding = np.array(embedding).astype("float32").reshape(1, -1)
    distances, indices = index.search(embedding, top_k)
    
    return [image_map[i] for i in indices[0] if i in image_map]
