## input:

```
def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:
&#x20;   """Return the chunks of every .py file under \`root\`, including subfolders.
&#x20;   Process the files in order of their relative path, written with forward slashes
&#x20;   and sorted as plain strings. Keep each file's chunks in file order.
&#x20;   For the requests codebase this returns 230 chunks.
&#x20;   """
Write `split_file` and `split_corpus` in `askcode/split.py`, using Python's built-in `ast` module. A method becomes a chunk named `ClassName.method_name`; decorators belong to the function they decorate; code outside functions is not a chunk. The six rules are in the docstring. For the requests code your splitter must produce 230 chunks, and `SessionRedirectMixin.should_strip_auth` must run from line 127 to line 157 of sessions.py.


tests:
"""Public tests for Step 2 (askcode/split.py). Run: pytest tests/test_split.py"""

from pathlib import Path

from askcode import CORPUS_DIR
from askcode.split import split_corpus, split_file


def write(tmp_path: Path, relative: str, source: str) -> Path:
&#x20;   path = tmp_path / relative
&#x20;   path.parent.mkdir(parents=True, exist_ok=True)
&#x20;   path.write_text(source, encoding="utf-8")
&#x20;   return path


SAMPLE = (
&#x20;   "import os\n"                     # 1
&#x20;   "\n"                              # 2
&#x20;   "LIMIT = 3\n"                     # 3
&#x20;   "\n"                              # 4
&#x20;   "def top(x):\n"                   # 5
&#x20;   "    return x + 1\n"              # 6
&#x20;   "\n"                              # 7
&#x20;   "class Box:\n"                    # 8
&#x20;   "    size = 2\n"                  # 9
&#x20;   "\n"                              # 10
&#x20;   "    def open(self):\n"           # 11
&#x20;   "        return 'open'\n"         # 12
&#x20;   "\n"                              # 13
&#x20;   "    @property\n"                 # 14
&#x20;   "    def label(self):\n"          # 15
&#x20;   "        return 'box'\n"          # 16
)


def test_names_for_functions_and_methods(tmp_path):
&#x20;   path = write(tmp_path, "sample.py", SAMPLE)
&#x20;   assert [c.name for c in split_file(path, tmp_path)] == ["top", "Box.open", "Box.label"]


def test_line_numbers_and_exact_text(tmp_path):
&#x20;   path = write(tmp_path, "sample.py", SAMPLE)
&#x20;   top, box_open, \_ = split_file(path, tmp_path)
&#x20;   assert (top.start_line, top.end_line) == (5, 6)
&#x20;   assert top.text == "def top(x):\n    return x + 1"
&#x20;   assert (box_open.start_line, box_open.end_line) == (11, 12)
&#x20;   assert box_open.text == "    def open(self):\n        return 'open'"


def test_decorator_line_starts_the_chunk(tmp_path):
&#x20;   path = write(tmp_path, "sample.py", SAMPLE)
&#x20;   label = split_file(path, tmp_path)[2]
&#x20;   assert (label.start_line, label.end_line) == (14, 16)
&#x20;   assert label.text.split("\n")[0] == "    @property"


def test_file_is_relative_with_forward_slashes(tmp_path):
&#x20;   path = write(tmp_path, "pkg/inner/mod.py", "def f():\n    pass\n")
&#x20;   assert split_file(path, tmp_path)[0].file == "pkg/inner/mod.py"


def test_code_outside_functions_is_not_a_chunk(tmp_path):
&#x20;   path = write(tmp_path, "consts.py", "A = 1\nB = 2\n\nclass Empty:\n    pass\n")
&#x20;   assert split_file(path, tmp_path) == []


def test_corpus_has_230_chunks():
&#x20;   assert len(split_corpus(CORPUS_DIR)) == 230


def test_corpus_known_method():
&#x20;   chunks = split_corpus(CORPUS_DIR)
&#x20;   found = [c for c in chunks if c.name == "SessionRedirectMixin.should_strip_auth"]
&#x20;   assert len(found) == 1
&#x20;   chunk = found[0]
&#x20;   assert (chunk.file, chunk.start_line, chunk.end_line) == ("sessions.py", 127, 157)
&#x20;   assert chunk.text.split("\n")[0].strip() == "def should_strip_auth(self, old_url, new_url):"


def test_corpus_order_is_by_file_then_line():
&#x20;   chunks = split_corpus(CORPUS_DIR)
&#x20;   keys = [(c.file, c.start_line) for c in chunks]
&#x20;   assert keys == sorted(keys)

implement split corpus
```

## output:

```
Add the following implementation to askcode/split.py. It uses Python's built-in ast module and preserves exact source text, including decorators and indentation.
    tree = ast.parse(source, filename=str(path))    relative_path = path.relative_to(root).as_posix()    chunks = []    def add_chunk(node, name: str) -> None:        start = node.lineno        # Include every decorator in the function's chunk.        if node.decorator_list:            start = min(                start,                *(decorator.lineno for decorator in node.decorator_list),            )        end = node.end_lineno        chunks.append(            Chunk(                file=relative_path,                name=name,                start_line=start,                end_line=end,                text="\n".join(lines[start - 1:end]),            )        )    function_types = (ast.FunctionDef, ast.AsyncFunctionDef)    for node in tree.body:        if isinstance(node, function_types):            add_chunk(node, node.name)        elif isinstance(node, ast.ClassDef):            for child in node.body:                if isinstance(child, function_types):                    add_chunk(child, f"{node.name}.{child.name}")    return sorted(chunks, key=lambda chunk: chunk.start_line)def split_corpus(root: Path = CORPUS_DIR) -> list[Chunk]:    """Return chunks of every .py file under root, including subfolders.    Process files in order of their relative path, written with forward    slashes and sorted as plain strings. Keep each file's chunks in    file order.    For the requests codebase this returns 230 chunks.    """    paths = sorted(        root.rglob("*.py"),        key=lambda path: path.relative_to(root).as_posix(),    )    chunks = []    for path in paths:        chunks.extend(split_file(path, root))    return chunks



Key implementation details
- rglob("*.py") recursively discovers Python files.
- relative_to(root).as_posix() ensures forward-slash paths.
- ast.parse() identifies functions and class methods.
- decorator_list ensures chunks begin at the first decorator.
- end_lineno gives the inclusive final source line.
- lines[start - 1:end] preserves the exact source text without trailing newlines.
- File sorting and per-file line sorting produce deterministic corpus ordering.
The implementation handles synchronous and asynchronous functions. It excludes imports, assignments, standalone class definitions, and other code outside functions.
It also leaves nested function definitions inside their enclosing function's chunk rather than creating duplicate chunks for them.
Verification: The repository was not attached, so I could not execute the 230-chunk corpus test. You can run:
pytest tests/test_split.py -v
```
