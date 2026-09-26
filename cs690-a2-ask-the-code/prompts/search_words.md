## input: 
```
Step 3. Search by words (45 minutes)

In lecture we covered keyword search, and what it misses.

Write search_words in askcode/search_words.py. A chunk scores points for every question word it contains, and rare words score more than common ones. In this codebase, "authorization" appears in 8 of the 230 functions, so it weighs log(230 / 8) = 3.36; "self" appears in 155, so it weighs only log(230 / 155) = 0.39. The exact formula is in the docstring.

Then run the first experiment. It makes no AI calls and costs nothing:

python -m askcode.run_eval --search words --no-ai

It writes results/retrieval_words.csv and prints how many of your answerable questions had the right function in the top 3.

"""Step 3: find the chunks that share the most useful words with the question.

YOUR CODE. Read HANDOUT.md, Step 3, first.
Check your work with:  pytest tests/test_search_words.py
"""

from __future__ import annotations

import math  # noqa: F401  (you will need it)

from askcode.core import STOPWORDS, Chunk, words  # noqa: F401


def search_words(question: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:
    """Return up to k chunks that best match the question by shared words.

    Scoring. The tests check the exact order this produces.

    1. Question words: the set of words(question), minus STOPWORDS.
    2. Chunk words: for each chunk, the set of words(chunk.name + "\\n" + chunk.text).
    3. For each question word w, df(w) is the number of chunks whose word set
       contains w, and N is len(chunks). Ignore question words no chunk contains.
    4. weight(w) = math.log(N / df(w)). A rare word weighs a lot; a word found in
       every chunk weighs 0.
    5. score(chunk) = the sum of weight(w) over the question words the chunk contains,
       rounded with round(score, 6). Rounding makes chunks that match the same words
       tie exactly, whatever order your code adds the weights in.
    6. Return the chunks whose score is greater than 0, highest score first, at most k
       of them. When two chunks have the same score, the one that comes first in
       `chunks` comes first.

    If the question has no words left after step 1, or chunks is empty, return [].

    This is the core idea of BM25, the standard keyword search (slide 45). BM25 adds
    adjustments for how often a word repeats and for chunk length.
    """
    raise NotImplementedError("Step 3: write search_words in askcode/search_words.py")

"""Public tests for Step 3 (askcode/search_words.py). Run: pytest tests/test_search_words.py"""

from askcode import CORPUS_DIR
from askcode.core import Chunk
from askcode.search_words import search_words
from askcode.split import split_corpus


def chunk(name: str, text: str) -> Chunk:
    return Chunk(file="demo.py", name=name, start_line=1, end_line=1, text=text)


CHUNKS = [
    chunk("open_session", "session = make_session()"),
    chunk("close_session", "session.close()"),
    chunk("digest_login", "session digest nonce"),
    chunk("render_page", "html template"),
]


def test_rare_word_outranks_common_word():
    # "digest" is in 1 chunk, "session" is in 3, so the digest chunk must come first.
    result = search_words("digest session", CHUNKS, k=4)
    assert [c.name for c in result] == ["digest_login", "open_session", "close_session"]


def test_chunks_with_no_shared_word_are_left_out():
    assert [c.name for c in search_words("template", CHUNKS, k=3)] == ["render_page"]


def test_at_most_k():
    assert len(search_words("session", CHUNKS, k=2)) == 2


def test_ties_keep_the_original_order():
    result = search_words("session", CHUNKS, k=3)
    assert [c.name for c in result] == ["open_session", "close_session", "digest_login"]


def test_only_stopwords_gives_nothing():
    assert search_words("what is the", CHUNKS, k=3) == []


def test_function_names_count_as_words():
    # "render" appears only in a chunk's name, not in its text.
    assert [c.name for c in search_words("render", CHUNKS, k=3)] == ["render_page"]


def test_corpus_redirect_question_finds_should_strip_auth_first():
    chunks = split_corpus(CORPUS_DIR)
    result = search_words("strip the Authorization header on redirect", chunks, k=3)
    assert result[0].name == "SessionRedirectMixin.should_strip_auth"
    assert len(result) == 3
```

## output 
```
Replace the raise NotImplementedError(...) line in askcode/search_words.py with the following implementation. It follows the exact scoring formula, rounds scores to six decimal places, excludes zero-score chunks, and preserves original order when scores tie.





def search_words(question: str, chunks: list[Chunk], k: int = 3) -> list[Chunk]:    """Return up to k chunks that best match the question by shared words."""    if not chunks or k <= 0:        return []    # 1. Extract question words, excluding stopwords.    question_words = set(words(question)) - STOPWORDS    if not question_words:        return []    # 2. Extract each chunk's unique words, including its function name.    chunk_words = [        set(words(chunk.name + "\n" + chunk.text))        for chunk in chunks    ]    # 3. Calculate document frequency for each question word.    df = {        w: sum(w in cw for cw in chunk_words)        for w in question_words    }    # 4. Calculate inverse document frequency (IDF).    N = len(chunks)    weights = {        w: math.log(N / count)        for w, count in df.items()        if count > 0    }    # 5. Score each chunk and preserve its original index.    scored = []



Run the tests
From your project root:

pytest tests/test_search_words.py



Run the first experiment
Once the tests pass:

python -m askcode.run_eval --search words --no-ai



This evaluates keyword retrieval without making AI calls and writes the results to:
results/retrieval_words.csv
The printed top-3 metric tells you how often the correct function appears among the first three retrieved chunks for your answerable questions.
```