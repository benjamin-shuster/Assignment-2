## Input

```
"""Step 4, part A: the five-part prompt from the Week 3 slides.\
\
YOUR CODE. Read HANDOUT.md, Step 4, first.\
Check your work with:  pytest tests/test_prompt.py\
"""\
\
from \_\_future\_\_ import annotations\
\
from askcode.core import NO_CODE, Chunk, Prompt, format_chunk  # noqa: F401\
\
\
def build_prompt_five_part(question: str, chunks: list[Chunk]) -> Prompt:\
&#x20;   """Build the prompt your pipeline sends to the AI.\
\
&#x20;   Requirements. The tests check each one.\
\
&#x20;   1\. prompt.system holds the five parts from slide 6. Each part starts on its own\
&#x20;      line with its label, in this order:\
&#x20;          Goal:\
&#x20;          Inputs and outputs:\
&#x20;          Rules:\
&#x20;          Example:\
&#x20;          Reply format:\
&#x20;   2\. Rules tell the model to answer only from the code shown, and, when that code\
&#x20;      does not answer the question, to reply with the answer\
&#x20;      "not found in the code shown" and null for both file and line.\
&#x20;   3\. Example holds one sample question and its correct reply written as a JSON\
&#x20;      object with the keys "answer", "file" and "line". Do not use one of your own\
&#x20;      ten questions.\
&#x20;   4\. Reply format asks for exactly one JSON object with the keys "answer" (a string),\
&#x20;      "file" (a string or null) and "line" (an integer or null), with nothing before\
&#x20;      or after it.\
&#x20;   5\. prompt.system is the same text for every question and every set of chunks.\
&#x20;      It is the stable part of the prompt, so it goes first (slide 26).\
&#x20;   6\. prompt.user is a line "Code:", then every chunk shown with format_chunk(chunk)\
&#x20;      in the order given, separated by blank lines, then a line "Question:", then\
&#x20;      the question. The question comes last. If chunks is empty, put NO_CODE under\
&#x20;      "Code:" instead.\
&#x20;   """\
&#x20;   raise NotImplementedError("Step 4: write build_prompt_five_part in askcode/prompt.py")





In lecture we covered the five parts of a prompt, standing instructions and why the stable part goes first, and getting JSON your program can use, including what a schema does not buy you.

Part A. Write `build_prompt_five_part` in `askcode/prompt.py`. The prompt has two parts:

- `system`: the five labeled parts (Goal, Inputs and outputs, Rules, Example, Reply format). It is the same for every question, so it goes first.
- `user`: the code, then the question, last.

Your rules must say what to do when the code shown does not answer the question: reply "not found in the code shown" with null file and line.





"""Public tests for Step 4, part A (askcode/prompt.py). Run: pytest tests/test_prompt.py"""



import json

import re



from askcode.core import NO_CODE, Chunk, format_chunk

from askcode.prompt import build_prompt_five_part



LABELS = ["Goal:", "Inputs and outputs:", "Rules:", "Example:", "Reply format:"]



A = Chunk(file="sessions.py", name="Session.close", start_line=10, end_line=11, text="def close(self):\n    pass")

B = Chunk(file="api.py", name="get", start_line=60, end_line=61, text="def get(url):\n    return url")





def label_positions(system: str) -> list[int]:

&#x20;   positions = []

&#x20;   for label in LABELS:

&#x20;       match = re.search(r"(?m)^" + re.escape(label), system)

&#x20;       assert match, f"prompt.system has no line starting with {label!r}"

&#x20;       positions.append(match.start())

&#x20;   return positions





def test_five_labels_in_order():

&#x20;   positions = label_positions(build_prompt_five_part("Where is close?", [A]).system)

&#x20;   assert positions == sorted(positions)





def test_system_is_the_same_for_every_question_and_every_context():

&#x20;   first = build_prompt_five_part("Where is close?", [A]).system

&#x20;   assert build_prompt_five_part("How does get work?", [B, A]).system == first

&#x20;   assert build_prompt_five_part("Anything?", []).system == first





def test_rules_cover_the_not_found_case():

&#x20;   system = build_prompt_five_part("q", [A]).system

&#x20;   assert "not found in the code shown" in system

&#x20;   assert "null" in system





def test_reply_format_names_the_three_keys():

&#x20;   system = build_prompt_five_part("q", [A]).system

&#x20;   reply_format = system[label_positions(system)[4]:]

&#x20;   for key in ('"answer"', '"file"', '"line"'):

&#x20;       assert key in reply_format





def test_example_contains_a_valid_json_reply():

&#x20;   system = build_prompt_five_part("q", [A]).system

&#x20;   starts = label_positions(system)

&#x20;   example = system[starts[3]:starts[4]]

&#x20;   replies = []

&#x20;   for candidate in re.findall(r"**\\{**[^{}]\***\\}**", example):

&#x20;       try:

&#x20;           replies.append(json.loads(candidate))

&#x20;       except json.JSONDecodeError:

&#x20;           pass

&#x20;   assert any(isinstance(r, dict) and set(r) == {"answer", "file", "line"} for r in replies)





def test_user_has_code_then_question_last():

&#x20;   question = "How does get work?"

&#x20;   user = build_prompt_five_part(question, [A, B]).user

&#x20;   code_at = user.index("Code:")

&#x20;   a_at, b_at = user.index(format_chunk(A)), user.index(format_chunk(B))

&#x20;   question_label_at = user.index("Question:")

&#x20;   assert code_at < a_at < b_at < question_label_at

&#x20;   assert user.rstrip().endswith(question)


def test_empty_context_says_no_code():

&#x20;   user = build_prompt_five_part("Anything?", []).user

&#x20;   assert NO_CODE in user

&#x20;   assert user.index("Code:") < user.index(NO_CODE) < user.index("Question:")

\
```

## Output

```
Replace the raise NotImplementedError(...) line in askcode/prompt.py with the implementation below.
The function keeps the five standing instructions in system and places the code and question in user, with the question last.
Complete implementation
from __future__ import annotationsfrom askcode.core import NO_CODE, Chunk, Prompt, format_chunk  # noqa: F401def build_prompt_five_part(question: str, chunks: list[Chunk]) -> Prompt:    """Build the five-part prompt sent to the AI."""    system = """Goal:Answer questions about a codebase using only the provided code.Inputs and outputs:You receive code chunks with file names and line numbers, followed by a question.Return an answer supported by the provided code, including its file and line number.Rules:Answer only from the code shown.Do not guess, invent information, or use outside knowledge.If the code shown does not answer the question, reply with"not found in the code shown" as the answer, and null for both file and line.Only cite a file and line number that appear in the provided code.Example:Question: What does the following function return?Code:File: math_utils.pyLine 5: def double(x):Line 6:     return x * 2Reply:{"answer": "The function returns x multiplied by 2.", "file": "math_utils.py", "line": 6}Reply format:Return exactly one JSON object with these keys:"answer": a string containing the answer."file": a string containing the source filename, or null."line": an integer containing the source line number, or null.Do not include Markdown, code fences, explanations, or any text before or after the JSON object."""    code = "\n\n".join(format_chunk(chunk) for chunk in chunks)    if not chunks:        code = NO_CODE    user = f"Code:\n{code}\n\nQuestion:\n{question}"    return Prompt(system=system, user=user)



Why this meets the requirements
Requirement	Implementation
Five labeled parts	All five appear in the required order.
No unsupported answers	Rules explicitly prohibit guessing.
Not-found behavior	Uses the exact required answer and null values.
JSON example	Contains "answer", "file", and "line".
Stable system prompt	Does not depend on question or chunks.
Code formatting	Uses format_chunk(chunk) in the supplied order.
Empty context	Uses NO_CODE.
Question last	Places the question at the end of user.
The implementation follows the uploaded lecture's guidance on five-part prompts, stable instructions first, and JSON output.
Run the tests
From the project root:

pytest tests/test_prompt.py



Expected result: The implementation is designed to satisfy all seven public tests you provided.
I could not execute the actual project tests because HANDOUT.md, askcode/core.py, and the test files were not included in the upload. Only the lecture slides and pasted test code were available.

```
