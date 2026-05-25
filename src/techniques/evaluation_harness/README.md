# Evaluation Harness

## What this demonstrates

A tiny evaluator that scores one model answer against a rubric, with a deterministic local fallback and optional LLM judge.

## Why your hackathon project might want it

Use this when the team needs evidence that the assistant is improving, not just a good-looking demo. It maps to evaluation and responsible-AI lessons and fits every sample track.

## Run it locally

```bash
cd src/techniques/evaluation_harness
python example.py
```

No Azure credentials are required; the local evaluator returns a stable score.

## Read it line-by-line

The example defines one test case, checks groundedness and brevity locally, and can switch to `gpt-4o-mini` JSON judging when Azure is configured.

## Extend it

- What five test questions would reveal your assistant's biggest weakness?
- Which rubric dimension should be a hard fail for your domain?
- How would you store evaluation results after each prompt change?
- What should tutors review manually even if the score is high?

## Watch out for

- Symptom: scores rise but answers get worse. Cause: the rubric rewards the wrong behavior. Fix: add real failure cases.
- Symptom: judge output is not JSON. Cause: no structured-output requirement. Fix: use JSON mode and validate fields.
- Symptom: teams overfit to one test. Cause: tiny eval set. Fix: add at least one easy, one hard, and one refusal case.

## Where to go next

- Public deep dive: https://koica-tiu.halla.ai/hackathon/samples/evaluation-harness
- Technique catalog: ../../../../docs/TECHNIQUES.md
- Microsoft Learn: https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai
