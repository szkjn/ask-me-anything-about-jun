import faiss
import numpy as np
import json
from app.utils.config import EMBEDDINGS_FILE, INDEX_FILE, FILENAMES_FILE

# Load embeddings from the JSON file
with open(EMBEDDINGS_FILE, "r") as f:
    embeddings_data = json.load(f)

# Prepare data for FAISS
filenames = list(embeddings_data.keys())
embeddings = np.array(
    [embedding for embedding in embeddings_data.values()], dtype="float32"
)

# Create a FAISS index
dimension = embeddings.shape[1]  # Dimensionality of the embeddings
index = faiss.IndexFlatL2(dimension)  # L2 distance metric
index.add(embeddings)

# Save the FAISS index and filenames
faiss.write_index(index, INDEX_FILE)
with open(FILENAMES_FILE, "w") as f:
    json.dump(filenames, f)

print("FAISS index and filenames saved.")
