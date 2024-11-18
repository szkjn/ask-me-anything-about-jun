import os

# Input files
EMBEDDINGS_FILE = os.path.abspath("embeddings/embeddings.json")

# Output files
INDEX_FILE = os.path.abspath("models/embeddings.index")
FILENAMES_FILE = os.path.abspath("models/filenames.json")

# Data files
DATA_FOLDER = os.path.abspath("../data/")

# API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY_HAVANA")
