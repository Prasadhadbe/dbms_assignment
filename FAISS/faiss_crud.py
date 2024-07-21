import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the pre-trained model for generating embeddings
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class FaissCRUD:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.id_to_index = {}  
        self.index_to_id = {}  
        self.embeddings = []   
        self.ids = []          
        self.next_index = 0    

    def create(self, id, text):
        embedding = model.encode([text]).astype(np.float32)
        self.index.add(embedding)
        self.id_to_index[id] = self.next_index
        self.index_to_id[self.next_index] = id
        self.embeddings.append(embedding)
        self.ids.append(id)
        self.next_index += 1

    def read(self, text, k=1):
        embedding = model.encode([text]).astype(np.float32)
        distances, indices = self.index.search(embedding, k)
        return distances, indices

    def update(self, id, new_text):
        if id in self.id_to_index:
            idx = self.id_to_index[id]
            new_embedding = model.encode([new_text]).astype(np.float32)
            self.embeddings[idx] = new_embedding
            self.rebuild_index()
        else:
            raise ValueError("ID not found")

    def delete(self, id):
        if id in self.id_to_index:
            idx = self.id_to_index.pop(id)
            self.index_to_id.pop(idx)
            self.embeddings.pop(idx)
            self.ids.pop(idx)
            self.rebuild_index()
        else:
            raise ValueError("ID not found")

    def rebuild_index(self):
        self.index = faiss.IndexFlatL2(self.dimension)  
        if self.embeddings:
            self.index.add(np.vstack(self.embeddings))  
            self.id_to_index = {id: idx for idx, id in enumerate(self.ids)}
            self.index_to_id = {idx: id for idx, id in enumerate(self.ids)}
            self.next_index = len(self.embeddings)
        else:
            self.next_index = 0

faiss_crud = FaissCRUD()
