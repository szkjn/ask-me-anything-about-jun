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

EXAMPLE_QUESTIONS = [
    "Do you have experience in data engineering ?",
    "For how long have you been working in AI ?",
    "What have you been up to lately ?"
]