"""Step 4, part B: check the AI's reply before your program trusts it.

YOUR CODE. Read HANDOUT.md, Step 4, first.
Check your work with:  pytest tests/test_answer.py
"""

from __future__ import annotations

import json  # noqa: F401  (you will need it)

from askcode.core import BadReply  # noqa: F401  (raise this for every bad reply)


def parse_reply(text: str) -> dict:
    """Check the model's reply and return {"answer": ..., "file": ..., "line": ...}.

    Accept the reply only if every rule holds. Otherwise raise BadReply with a short
    message that says which rule failed. Never let a different exception escape.

    1. After stripping whitespace, the reply is one JSON object. The only thing
       allowed around it is a single Markdown code fence: a first line of ``` or
       ```json, and a last line of ```. Any other text before or after the object
       makes the reply bad.
    2. The object has exactly the keys "answer", "file" and "line": none missing,
       none extra.
    3. "answer" is a string that is not empty or only whitespace.
    4. "file" is a non-empty string or null. "line" is an integer or null; true and
       false do not count as integers, and an integer line must be at least 1.
    5. "file" and "line" are both null, or both set.

    Return a new dict with exactly the three keys and the values from the reply.
    """
    try:
        text = text.strip()

        # Remove an optional Markdown code fence.
        if text.startswith("```"):
            lines = text.splitlines()

            if (
                len(lines) < 3
                or lines[0] not in ("```", "```json")
                or lines[-1] != "```"
            ):
                raise BadReply("Invalid Markdown code fence")

            text = "\n".join(lines[1:-1])

        # Require exactly one valid JSON object.
        try:
            data = json.loads(text)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            raise BadReply("Invalid JSON") from exc

        if not isinstance(data, dict):
            raise BadReply("Reply must be a JSON object")

        # Require exactly the specified keys.
        if set(data.keys()) != {"answer", "file", "line"}:
            raise BadReply("Incorrect keys")

        answer = data["answer"]
        file = data["file"]
        line = data["line"]

        # Validate answer.
        if not isinstance(answer, str) or not answer.strip():
            raise BadReply("Answer must be a non-empty string")

        # Validate file.
        if file is not None:
            if not isinstance(file, str) or not file:
                raise BadReply("File must be a non-empty string or null")

        # Validate line. Explicitly reject booleans.
        if line is not None:
            if type(line) is not int or line < 1:
                raise BadReply("Line must be a positive integer or null")

        # File and line must either both be null or both be set.
        if (file is None) != (line is None):
            raise BadReply("File and line must both be set or both be null")

        return {
            "answer": answer,
            "file": file,
            "line": line,
        }

    except BadReply:
        raise
    except Exception as exc:
        raise BadReply("Invalid reply") from exc
