"""Step 7: find chunks by meaning instead of by shared words.

YOUR CODE. Read HANDOUT.md, Step 7, first.
Check your work with:  pytest tests/test_search_meaning.py

The embedding model runs on your own laptop (askcode/embed.py). It is free and needs
no key; the first run downloads it once, about 67 MB, into the .models folder.
"""

from __future__ import annotations

import math  # noqa: F401  (you will need it)
from collections.abc import Callable

from askcode import embed
from askcode.core import Chunk


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two vectors: dot(a, b) / (length(a) * length(b)).

    Return 0.0 if either vector has length 0 (all zeros).
    Raise ValueError if the two vectors do not have the same number of numbers.
    """

    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")

    dot_product = sum(x * y for x, y in zip(a, b))

    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))

    if length_a == 0 or length_b == 0:
        return 0.0

    return dot_product / (length_a * length_b)


class MeaningIndex:
    """Embed every chunk once, then answer many questions quickly (slides 43 to 46)."""

    def __init__(
        self,
        chunks: list[Chunk],
        embed_passages: Callable[[list[str]], list[list[float]]] | None = None,
        embed_query: Callable[[str], list[float]] | None = None,
    ) -> None:
        """Store the chunks and embed all of them, here, once.

        1. If embed_passages or embed_query is None, use embed.embed_passages or
           embed.embed_query. (The tests pass in small fake versions instead.)
        2. The text embedded for a chunk is chunk.name + "\\n" + chunk.text.
        3. Call embed_passages exactly once, with the list of all those texts in the
           order of `chunks`. One call is far faster than one call per chunk.
        4. Keep what you need for search: the chunks, their vectors, and embed_query.
        """

        if embed_passages is None:
            embed_passages = embed.embed_passages

        if embed_query is None:
            embed_query = embed.embed_query

        self.chunks = chunks
        self.embed_query = embed_query

        texts = [
            chunk.name + "\n" + chunk.text
            for chunk in chunks
        ]

        self.vectors = embed_passages(texts)

    def search(self, question: str, k: int = 3) -> list[Chunk]:
        """Return the k chunks whose vectors are closest in meaning to the question.

        1. Embed the question with embed_query, once. Do not embed any chunk here.
        2. Score every chunk with cosine(question vector, chunk vector).
        3. Return the k highest-scoring chunks, highest first. When two chunks have
           the same score, the one that comes first in the chunks list comes first.

        Unlike word search, this always returns k chunks (or every chunk, if there
        are fewer than k), even when none of them is relevant (slide 56).
        """
        question_vector = self.embed_query(question)

        scores = [
            cosine(question_vector, vector)
            for vector in self.vectors
        ]

        ranked_indices = sorted(
            range(len(self.chunks)),
            key=lambda i: scores[i],
            reverse=True,
        )

        return [
            self.chunks[i]
            for i in ranked_indices[:k]
        ]
