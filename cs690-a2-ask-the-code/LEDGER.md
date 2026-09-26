# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates and numbers are made up.

```
## Entry 2
artifact:  askcode/split.py at commit 3f2a9c1
tool:      GitHub Copilot Chat in VS Code, model Claude Haiku 4.5, 2026-09-22
prompts:   asked for an ast loop that returns methods with class-qualified names;
           prompts/split-01.md
review:    read every line; rejected its use of ast.walk, which also returned nested
           functions and broke rule 1; rewrote the loop over tree.body and class bodies
           myself; kept its decorator handling after checking it against rule 3
checks:    pytest tests/test_split.py: 8 passed
evidence:  HANDOUT Step 2, split.py docstring rules 1 to 6
risk:      I did not test a file with Windows line endings

## Entry 5
artifact:  results/top3_words_five_part.csv at commit 8d41e07
tool:      askcode run_eval, anthropic claude-haiku-4-5-20251001, 2026-09-23
prompts:   the five-part prompt in askcode/prompt.py at commit 8d41e07;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part:
           valid JSON 10 of 10, right place 6 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit 51c0e2a; corpus requests v2.32.3
result:    correct 6 of 10, 24,113 input tokens; results/top3_words_five_part.csv
changed:   two misses were retrieval failures, so I looked at why word search missed
           them before touching the prompt
```

## My entries

## Entry 1
artifact:  askcode/split.py at 7ca0bb12418ef35efe33c48ea5f8e7464a1bd10b
tool: Open AI chat GPT via web ui
prompts: `prompts/split_file.md` . I know I am supposed to make a detailed prompt, but the doc string has most of the necessary information.
review: skimed the output to ensure its safe to run and not doing anything harmful, and then ran the tests to ensure correctness
checks: `pytest tests/test_split.py`, and the only failed test were due to the NotImplementedError for the split_corpus function.
evidence: HANDOUT Step 2, doc string
risk: low risk, reviewed manualy
changes: discarded code and used output from the Entry 2

## Entry 2
artifact:  askcode/split.py at 7ca0bb12418ef35efe33c48ea5f8e7464a1bd10b
tool: Open AI chat GPT via web ui
prompts: `prompts/split_corpus.md`.
review: skimed the output to ensure its safe to run and not doing anything harmful, and then ran the tests to ensure correctness
checks: `pytest tests/test_split.py`, and this time, all tests passed.
evidence: HANDOUT Step 2, tests
risk: low risk, reviewed manualy
    
## Entry 3
artifact:  askcode/search_words.py at fee95a9746d1bc8f90340419c80c9b88eefcbf87
tool: Open AI chat GPT via web ui
prompts: `prompts/search_words.md`.
review: focused more on the comments and logic in the code to ensure it correctly implements the search_words algorithm.
checks: `pytest tests/test_search_words.py`, and all tests passed.
evidence: HANDOUT Step 3
risk: low risk, reviewed manualy

## Entry 4
artifact:  askcode/prompt.py at b1eed5e0ce5475afc6c863ad344d5bff3cc3c18c
tool: Open AI chat GPT via web ui
prompts: `prompts/prompt.md`.
review: Compared the system prompt with slide 11 to ensure all 5 steps are mentioned. Read the code to ensure I understand the implementation.
checks: `pytest tests/test_prompt.py`, and all tests passed.
evidence: HANDOUT Step 4 part A
risk: low risk, reviewed manualy
attachments used in the prompt: CS690_Week4_Prompting_Context_Retrieval.pptx from canvas

## Entry 5
artifact:  askcode/answer.py at b09e9b21d40dfddc4da0e79c0c4186fa4032b49e
tool: Open AI chat GPT via web ui
prompts: `prompts/answer.md`.
review: read the code to ensure I understand the implementation.
checks: `pytest tests/test_answer.py`, and all tests passed.
evidence: HANDOUT Step 4 part B
risk: low risk, reviewed manualy

## Entry 6
artifact:  results/top3_words_five_part.csv at commit 0424fce22ccdc71ebceeaf6f21033eec1b912346
tool:      askcode run_eval, openai gpt-6-luna, 2026-09-26
prompts:   the five-part prompt in askcode/prompt.py at commit b1eed5e0ce5475afc6c863ad344d5bff3cc3c18c;
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part:
           valid JSON 10 of 10, right place 7 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit dbac75a0056b6bf5c07eef522ad504086c06ea4a; corpus requests v2.32.3
result:    correct 7 of 10, 16,371 in tokens, 1,014 out tokens; results/top3_words_five_part.csv

## Entry 7
artifact:  results/results/whole_five_part.csv at commit 0424fce22ccdc71ebceeaf6f21033eec1b912346
tool:      askcode run_eval, openai gpt-6-luna, 2026-09-26
prompts:   the five-part prompt in askcode/prompt.py at commit b1eed5e0ce5475afc6c863ad344d5bff3cc3c18c;
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --context whole --prompt five_part:
           valid JSON 10 of 10, right place 7 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit dbac75a0056b6bf5c07eef522ad504086c06ea4a; corpus requests v2.32.3
result:    correct 8 of 10, 547,713 in tokens, 1,605 out tokens; results/whole_five_part.csv


## Entry 8
artifact:  results/gold_five_part.csv.csv at commit 0424fce22ccdc71ebceeaf6f21033eec1b912346
tool:      askcode run_eval, openai gpt-6-luna, 2026-09-26
prompts:   the five-part prompt in askcode/prompt.py at commit b1eed5e0ce5475afc6c863ad344d5bff3cc3c18c;
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --context gold --prompt five_part:
           valid JSON 10 of 10, right place 10 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit dbac75a0056b6bf5c07eef522ad504086c06ea4a; corpus requests v2.32.3
result:    correct 10 of 10,  5,162 in tokens, 639 out tokens; results/gold_five_part.csv.csv

## Entry 9
artifact:  results/top3_words_minimal.csv at commit 15e9643f3e39aefaf7a26ad5f5b37fa6b9e3f852
tool:      askcode run_eval, openai gpt-6-luna, 2026-09-26
prompts:   the minimal prompt in build_prompt_minimal in core.py;
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt minimal
           valid JSON 0 of 10,
evidence:  HANDOUT Step 6
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit dbac75a0056b6bf5c07eef522ad504086c06ea4a; corpus requests v2.32.3
result:    correct 0 of 10,  13,883 in tokens, 2,714 out tokens; results/top3_words_minimal.csv
