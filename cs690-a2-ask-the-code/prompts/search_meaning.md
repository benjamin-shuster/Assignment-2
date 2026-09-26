## Input:
```
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
    raise NotImplementedError("Step 7: write cosine in askcode/search_meaning.py")


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
        raise NotImplementedError("Step 7: write MeaningIndex.__init__ in askcode/search_meaning.py")

    def search(self, question: str, k: int = 3) -> list[Chunk]:
        """Return the k chunks whose vectors are closest in meaning to the question.

        1. Embed the question with embed_query, once. Do not embed any chunk here.
        2. Score every chunk with cosine(question vector, chunk vector).
        3. Return the k highest-scoring chunks, highest first. When two chunks have
           the same score, the one that comes first in the chunks list comes first.

        Unlike word search, this always returns k chunks (or every chunk, if there
        are fewer than k), even when none of them is relevant (slide 56).
        """
        raise NotImplementedError("Step 7: write MeaningIndex.search in askcode/search_meaning.py")\
In lecture we covered embeddings, and why keyword search and meaning search fail in opposite directions.
Write cosine and MeaningIndex in askcode/search_meaning.py. The given embed.py turns text into 384 numbers with a small free model on your own laptop; texts with similar meaning get similar numbers. Your index embeds every function once, then scores each question against all of them with cosine similarity.
pytest tests/test_search_meaning.py
python -m askcode.run_eval --search meaning --no-ai

The first run downloads the model once, about 67 MB. It makes no AI calls and costs nothing. Then compare retrieval_meaning with retrieval_words in Tables 1 and 4 of python -m askcode.summary: which questions did each search find that the other missed?
"""Public tests for Step 7 (askcode/search_meaning.py). Run: pytest tests/test_search_meaning.py

These tests use tiny fake embedding functions, so they run without the real model.
"""

import math

import pytest

from askcode.core import Chunk
from askcode.search_meaning import MeaningIndex, cosine

TOPICS = ["redirect", "cookie", "proxy"]


def fake_vector(text: str) -> list[float]:
    lowered = text.lower()
    return [float(lowered.count(topic)) for topic in TOPICS]


class FakeModel:
    def __init__(self):
        self.passage_calls = []
        self.query_calls = []

    def passages(self, texts):
        self.passage_calls.append(list(texts))
        return [fake_vector(t) for t in texts]

    def query(self, text):
        self.query_calls.append(text)
        return fake_vector(text)


def chunk(name: str, text: str) -> Chunk:
    return Chunk(file="demo.py", name=name, start_line=1, end_line=1, text=text)


CHUNKS = [
    chunk("follow", "redirect redirect"),
    chunk("jar", "cookie"),
    chunk("route", "proxy proxy proxy"),
]


def test_cosine_values():
    assert cosine([1.0, 0.0], [2.0, 0.0]) == pytest.approx(1.0)
    assert cosine([1.0, 0.0], [0.0, 3.0]) == pytest.approx(0.0)
    assert cosine([1.0, 1.0], [1.0, 0.0]) == pytest.approx(1 / math.sqrt(2))


def test_cosine_zero_vector_is_zero():
    assert cosine([0.0, 0.0], [1.0, 2.0]) == 0.0


def test_cosine_length_mismatch():
    with pytest.raises(ValueError):
        cosine([1.0], [1.0, 2.0])


def test_chunks_are_embedded_once_with_name_and_text():
    model = FakeModel()
    MeaningIndex(CHUNKS, embed_passages=model.passages, embed_query=model.query)
    assert model.passage_calls == [["follow\nredirect redirect", "jar\ncookie", "route\nproxy proxy proxy"]]


def test_search_ranks_by_meaning_and_embeds_only_the_question():
    model = FakeModel()
    index = MeaningIndex(CHUNKS, embed_passages=model.passages, embed_query=model.query)
    result = index.search("which proxy is used", k=2)
    assert [c.name for c in result] == ["route", "follow"]
    assert model.query_calls == ["which proxy is used"]
    assert len(model.passage_calls) == 1


def test_search_always_returns_k():
    model = FakeModel()
    index = MeaningIndex(CHUNKS, embed_passages=model.passages, embed_query=model.query)
    assert len(index.search("nothing related at all", k=3)) == 3\
```
## Output:

Replace the three NotImplementedError statements with the implementation below.
The code uses cosine similarity, embeds all chunks once during initialization, and preserves the original chunk order when scores are tied.
from __future__ import annotationsimport mathfrom collections.abc import Callablefrom askcode import embedfrom askcode.core import Chunkdef cosine(a: list[float], b: list[float]) -> float:    """Calculate cosine similarity between two vectors."""    if len(a) != len(b):        raise ValueError("Vectors must have the same length")    dot_product = sum(x * y for x, y in zip(a, b))    length_a = math.sqrt(sum(x * x for x in a))    length_b = math.sqrt(sum(y * y for y in b))    if length_a == 0 or length_b == 0:        return 0.0    return dot_product / (length_a * length_b)class MeaningIndex:    """Embed every chunk once, then answer many questions quickly."""    def __init__(        self,        chunks: list[Chunk],        embed_passages: Callable[[list[str]], list[list[float]]] | None = None,        embed_query: Callable[[str], list[float]] | None = None,    ) -> None:



Why this satisfies the tests
Requirement	Implementation
Calculate dot product	sum(x * y ...)
Calculate vector lengths	math.sqrt(sum(x * x ...))
Handle zero vectors	Return 0.0
Handle mismatched dimensions	Raise ValueError
Embed each chunk with its name	chunk.name + "\n" + chunk.text
Embed all chunks in one call	embed_passages(texts)
Embed the question once	self.embed_query(question)
Rank by cosine similarity	Descending score
Preserve original order on ties	Python's stable sort
Return at most k chunks	ranked_indices[:k]
The important distinction is that chunks are embedded during initialization, not during search. Each new question requires only one query embedding.
Run your tests
From your project root, run:

pytest tests/test_search_meaning.py



Then evaluate meaning search:

python -m askcode.run_eval --search meaning --no-ai

python -m askcode.summary



The implementation is designed to satisfy the six supplied public tests. I couldn't run your project's tests or read HANDOUT.md because the project files weren't attached.
Comparing meaning search with keyword search
For the final lecture question, compare retrieval_meaning and retrieval_words in Tables 1 and 4 of the summary.
Look for these two cases:
- Meaning succeeds, words fails: The relevant function uses different vocabulary from the question. Embeddings can recognize related concepts without requiring identical words.
- Words succeeds, meaning fails: The question includes an exact function name, variable, identifier, or technical term. Keyword search may locate that exact match while embedding similarity retrieves a different function.
This illustrates why the methods fail in opposite directions: keyword search depends heavily on shared vocabulary, while meaning search can retrieve semantically similar but incorrect chunks.
The specific questions in your evaluation cannot be identified without the generated summary output
