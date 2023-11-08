# Document Embeddings

Based on the results of: https://arxiv.org/abs/2304.14796

## Implemented Methods

- Average Pooling, with adjustable range for sentences used.
- PERT weighted average pooling


## Usage

Wrapper for Sentence-Embedding, which is used to provide embedding functionality

```python

from sentence_transformers import SentenceTransformer

sentence_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

document_model = AverageDocumentEmbedding(sentence_model, language='german')


doc1 = "Arbitrary text"
doc2 = "..."

document_model.encode([doc1, doc2, ...])


```
