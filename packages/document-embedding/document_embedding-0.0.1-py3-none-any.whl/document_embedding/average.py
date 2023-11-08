from typing import List

import numpy as np

from document_embedding.base import DocumentEmbedding
from document_embedding.sentences import split_into_sentences


class AverageDocumentEmbedding(DocumentEmbedding):
    def __init__(self, sentence_model, language, range_start=0.0, range_stop=1.0):
        super().__init__(sentence_model, language)

        self.range_start = range_start
        self.range_stop = range_stop

    def _get_range(self, sentences: List[str]):
        index_start = int(self.range_start * len(sentences))
        index_stop = int(self.range_stop * len(sentences))
        return sentences[index_start:index_stop]

    def encode_single(self, document):
        return np.mean(
            self.model.encode(
                self._get_range(split_into_sentences(document, self.language))
            ),
            axis=0,
        )
