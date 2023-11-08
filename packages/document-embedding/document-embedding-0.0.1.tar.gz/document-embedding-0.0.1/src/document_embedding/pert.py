import numpy as np
from mcerp import PERT

from document_embedding.base import DocumentEmbedding
from document_embedding.sentences import split_into_sentences


def generate_dist(time_slots=16, pert_g=20, num_banks=100):
    # PERT is very slow (50ms per distribution) so we cache a bank of PERT distributions
    _xx = np.linspace(start=0, stop=1, num=time_slots)
    PERT_BANKS = []

    for _pp in np.linspace(0, 1, num=num_banks):
        if _pp == 0.5:  # some special case that makes g do nothing
            _pp += 0.001
        pert = PERT(low=-0.001, peak=_pp, high=1.001, g=pert_g, tag=None)
        _yy = pert.rv.pdf(_xx)
        _yy = _yy / sum(_yy)  # hack hack hack
        PERT_BANKS.append(_yy)

    return PERT_BANKS


class PertDocumentEmbedding(DocumentEmbedding):
    def __init__(
        self, sentence_model, language="english", time_slots=16, pert_g=20
    ) -> None:
        super().__init__(sentence_model, language)
        self.time_slots = time_slots
        self.pert_banks = generate_dist(time_slots, pert_g)

    def encode_single(self, document):
        sentence_embeddings = np.array(
            self.model.encode(split_into_sentences(document, self.language))
        )

        weights = 1.0 / np.array(len(sentence_embeddings))
        scaled_sentence_embeddings = np.multiply(sentence_embeddings.T, weights).T
        sentence_centers = np.linspace(0, 1, len(scaled_sentence_embeddings))
        sentence_location_weights = np.zeros((len(sentence_centers), self.time_slots))

        for i, center in enumerate(sentence_centers):
            bank_idx = int(center * (len(self.pert_banks) - 1))
            sentence_location_weights[i, :] = self.pert_banks[bank_idx]

        document_chunk_embedding = np.matmul(
            scaled_sentence_embeddings.T, sentence_location_weights
        ).T

        document_embedding = document_chunk_embedding.flatten()
        document_embedding = document_embedding / (
            np.linalg.norm(document_embedding) + 1e-5
        )

        return document_embedding
