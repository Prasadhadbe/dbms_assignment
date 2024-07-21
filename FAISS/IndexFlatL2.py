import faiss
import numpy as np

# Initialize the FAISS index
dimension = 384 
index = faiss.IndexFlatL2(dimension)
