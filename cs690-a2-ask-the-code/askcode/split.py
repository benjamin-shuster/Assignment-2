"""Step 2: split the codebase into chunks, one per function or method.

YOUR CODE. Read HANDOUT.md, Step 2, first.
Check your work with:  pytest tests/test_split.py
"""

from __future__ import annotations

import ast  # noqa: F401  (you will need it)
from pathlib import Path

from askcode import CORPUS_DIR
from askcode.core import Chunk

import ast
from pathlib import Path

from askcode import CORPUS_DIR


def split_file(path: Path, root: Path = CORPUS_DIR) -> list[Chunk]:
    """Split a Python file into function and method chunks."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source, filename=str(path))

    relative_path = path.relative_to(root).as_posix()
    chunks = []

    def add_chunk(node, name: str) -> None:
        start = node.lineno

        # Include every decorator in the function's chunk.
        if node.decorator_list:
            start = min(
                start,
                *(decorator.lineno for decorator in node.decorator_list),
            )

        end = node.end_lineno

        chunks.append(
            Chunk(
                file=relative_path,
                name=name,
                start_line=start,
                end_line=end,
                text="\n".join(lines[start - 1:end]),
            )
        )

    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)

    for node in tree.body:
        if isinstance(node, function_types):
            add_chunk(node, node.name)

        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, function_types):
                    add_chunk(child, f"{node.name}.{child.name}")

    return sorted(chunks, key=lambda chunk: chunk.start_line)


def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:
    """Return chunks of every .py file under root, including subfolders.

    Process files in order of their relative path, written with forward
    slashes and sorted as plain strings. Keep each file's chunks in
    file order.

    For the requests codebase this returns 230 chunks.
    """
    paths = sorted(
        root.rglob("*.py"),
        key=lambda path: path.relative_to(root).as_posix(),
    )

    chunks = []

    for path in paths:
        chunks.extend(split_file(path, root))

    return chunks
