# Assignment 2 Report: Ask the Code

Name: Benjamin Shuster  
Provider and model: OpenAI, gpt-6-luna  
Prices used (per million tokens, input and output), and the page you found them on:  
* input: `$0.10 per million tokens`
* output: `$0.50 per million tokens`  
* source: [OpenAI pricing page](https://developers.openai.com/api/docs/pricing)

## Table 1. Finding the right function

Paste Table 1 from `python -m askcode.summary` here, exactly as printed.
| Run | Right function in top 3 |
| --- | --- |
| retrieval_words | 5 of 7 |
| retrieval_meaning | 6 of 7 |
## Table 2. Answers

Paste Table 2 from `python -m askcode.summary` here, exactly as printed.
| Run | Valid JSON | Right place | Correct (your marks) | Input tokens | Output tokens | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| top3_words_five_part | 10 of 10 | 7 of 10 | 7 of 10 | 16,371 | 1,014 | 0.0021 |
| whole_five_part | 10 of 10 | 7 of 10 | 8 of 10 | 547,713 | 1,605 | 0.0556 |
| gold_five_part | 10 of 10 | 10 of 10 | 10 of 10 | 5,162 | 639 | 0.0008 |
| top3_words_minimal | 0 of 10 | 0 of 10 | 0 of 10 | 13,883 | 2,714 | 0.0027 |
## 1. Whose fault is it? (Step 5)

One row for every question marked `no` in top3_words_five_part. Take the first three
columns from Table 3 of `python -m askcode.summary`. Fault is retrieval, generation or
both, following the rule in Step 5. Evidence is one sentence about what you saw in the
reply or the retrieved functions.

| Question | Hit in top 3 | Correct with gold context | Fault | Evidence |
| --- | --- | --- | ----- | -------- |
| q07 | no | yes | retrieval | sessions.py was retrived, and did not have the correct information needed |
| q08 | n/a | yes | generation | there was no information provided in the source code that knew the correct answer , but it might have been able to infer it from the context |
| q09 | no | yes | retrieval | This might have been due to the function being deprecated. I think it might be in part my fault for a bad question / refrencing a bad function|
## 2. Paste everything or search? (Step 5)

Compare top3_words_five_part with whole_five_part: correct answers, input tokens and cost
for each, from Table 2. In two or three sentences: did pasting the whole codebase give
better answers, and was the difference worth the price?

The whole codebase was slightly better in terms of correct answers, because it got one more correct answer than the top3_words_five_part run. However, the difference was not substantial enough to justify the significantly higher input tokens and cost.

## 3. Minimal prompt against five-part prompt (Step 6)

Which prompt did better on right place, and which on correct? Give both numbers for both
prompts. Name one question where the two prompts' replies differed, and say what
differed.

The minimal prompt performed far worse than the five-part prompt in both right place and correct categories. For example, in q07 ("What meathods are allowed in the request function?"), the five-part prompt got it wrong and said it could not find it, while the minimal prompt made an incorect response. This suggests that providing more context and structure in the prompt improves the model's ability to understand the context of where its working, what it knows, and what it does not know.

|             | five-part prompt | minimal prompt |
|-------------|------------------|----------------|
| correct     | 7                | 0              |
| right place | 7                | 0              |

## 4. Word search against meaning search (Step 7)

Name one question meaning search ranked higher than word search, and one question word
search ranked higher than meaning search, with the ranks from Table 4 of
`python -m askcode.summary`. If no such question exists, say so. In one sentence each,
say why you think each search won.

| Question | Rank with words | Rank with meaning |
| --- | --- | --- |
| q01 | 2 | 1 |
| q03 | 1 | 1 |
| q04 | 1 | 1 |
| q06 | 1 | 2 |
| q07 | not in top 3 | not in top 3 |
| q09 | not in top 3 | 1 |
| q10 | 2 | 1 |

word > meaning - q06
meaning > word - q01

## 5. Your decision rule (Step 8)

One rule for this codebase: when would you paste everything, and when would you search?
Cite the measured cost and the measured correct count of both designs.

I would past the whole codebase when there are multiple relevant pieces of information scattered throughout the codebase (like how there were countless places that mention the list of HTTP methods), and I would use search when the relevant information is likely to be found in a specific part of the codebase, and when the cost of pasting the whole codebase would be prohibitively high without much benefit.

looking at whole_five_part and top3_words_five_part, while the outputs are very similar (both got 7 correct answers), the whole codebase approach used significantly more input tokens (547,713) instead of the search (16,371) and incurred a higher cost.