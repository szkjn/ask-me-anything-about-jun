import faiss
import numpy as np
import logging
import json
import os
from utils.config import INDEX_FILE, FILENAMES_FILE, DATA_FOLDER
from services.openai_service import OpenAIService


class FaissService:
    def __init__(self):
        self.index = self.load_index()
        self.filenames = self.load_filenames()
        self.document_map = self.load_documents()
        self.openai_service = OpenAIService()  # Instantiate OpenAIService here

    def load_index(self) -> faiss.swigfaiss_avx2.IndexFlatL2:
        """
        Loads the FAISS index from the disk.

        Returns:
            index: The loaded FAISS index.
        """
        try:
            index = faiss.read_index(INDEX_FILE)
            logging.info("FAISS index loaded successfully")
            return index
        except Exception as e:
            logging.error(f"Failed to load FAISS index: {e}")
            raise e

    def load_filenames(self) -> list:
        """
        Loads the filenames mapping from the disk.

        Returns:
            filenames: The loaded filenames mapping.
        """
        try:
            with open(FILENAMES_FILE, "r") as f:
                filenames = json.load(f)
            logging.info("Filenames mapping loaded successfully.")
            return filenames
        except Exception as e:
            logging.error(f"Failed to load filenames: {e}")
            raise e

    def load_documents(self) -> dict:
        """
        Loads the documents from the disk based on the filenames mapping.

        Returns:
            document_map: A dictionary mapping filenames to their corresponding documents.
        """
        document_map = {}
        for filename in self.filenames:
            file_path = os.path.join(DATA_FOLDER, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    document_map[filename] = file.read()
            else:
                logging.warning(f"Document {filename} does not exist.")
        return document_map

    def search_documents(self, question) -> str:
        """
        Searches for similar documents in three steps:
        1. Generates an embedding for the question using the OpenAIService.
        2. Uses the FAISS index to find the three most similar documents to the question embedding.
        3. Retrieves the content of the relevant documents from the document map.

        Args:
            question: The question to search for similar documents.

        Returns:
            context: The content of the three most similar documents.
        """
        query_embedding = np.array(
            self.generate_embedding(question), dtype="float32"
        ).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k=3)
        retrieved_docs = [self.filenames[idx] for idx in indices[0]]
        context = "\n\n".join(
            [
                self.document_map[doc]
                for doc in retrieved_docs
                if doc in self.document_map
            ]
        )

        return context

    def generate_embedding(self, question) -> list:
        # Use the OpenAIService instance to get the embedding for the question
        return self.openai_service.generate_embedding(question)
