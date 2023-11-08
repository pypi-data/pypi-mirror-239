from typing import cast

from nltk.data import load
from nltk.tokenize.punkt import PunktSentenceTokenizer


def split_into_sentences(content: str, language: str):
    tokenizer: PunktSentenceTokenizer = cast(
        PunktSentenceTokenizer, load(f"tokenizers/punkt/{language}.pickle")
    )

    return tokenizer.tokenize(content)
