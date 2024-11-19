"""
Description: This script is responsible for indexing the embeddings generated from the PDFs.
It uses the Facebook AI Similarity Search (FAISS) library to create an efficient index for the embeddings.
The index will be used in the retrieval process to find the most similar documents for a given query.
"""

import faiss
import numpy as np
import json
from app.utils.config import EMBEDDINGS_FILE, INDEX_FILE, FILENAMES_FILE

# Load embeddings from the JSON file
with open(EMBEDDINGS_FILE, "r") as f:
    embeddings_data = json.load(f)

"""
Prepares data for FAISS which requires embeddings to be in an array format.
Saves the filenames of the docs for later use in retrieving the most relevant docs.
"""
filenames = list(embeddings_data.keys())
embeddings = np.array(
    [embedding for embedding in embeddings_data.values()], dtype="float32"
)

"""
Creates a FAISS index:
Dimension is determined by the number of columns in the embeddings array.
Uses the L2 distance metric (common choice for similarity search).
"""
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

"""
Saves FAISS index as a binary file, and filenames as a JSON file.
These files will be used in the retrieval process.
"""
faiss.write_index(index, INDEX_FILE)

with open(FILENAMES_FILE, "w") as f:
    json.dump(filenames, f)

print("FAISS index and filenames saved.")
