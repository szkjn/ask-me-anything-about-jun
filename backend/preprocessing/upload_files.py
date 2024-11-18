import openai
import os
import json
from app.utils.config import OPENAI_API_KEY, EMBEDDINGS_FILE

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Directory containing Markdown files
DATA_FOLDER = "data/"
embeddings = {}

# Loop through `.md` files and generate embeddings
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".md"):
        filepath = os.path.join(DATA_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            # Generate embedding
            response = client.embeddings.create(
                input=content,
                model="text-embedding-3-small",  # Ensure correct model name
            )
            embeddings[filename] = response.data[0].embedding

# Save embeddings to a JSON file
with open(EMBEDDINGS_FILE, "w") as f:
    json.dump(embeddings, f)

print("Embeddings generated and saved to embeddings.json")
