from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class DocumentEmbedding:
    def __init__(self, sentence_model: SentenceTransformer, language="english") -> None:
        self.model = sentence_model
        self.language = language

    def output_dimension(self) -> int:
        raise NotImplementedError()

    def encode_single(self, document):
        raise NotImplementedError()

    def encode(self, documents: List[str]):
        if isinstance(documents, str):
            documents = [documents]

        embeddings = []

        for document in documents:
            embeddings.append(self.encode_single(document))

        return np.array(embeddings)
