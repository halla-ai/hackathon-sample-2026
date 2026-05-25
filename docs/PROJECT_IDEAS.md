# Project Ideas

These six ideas match the public sample pages and the technique scaffolds in [`docs/TECHNIQUES.md`](TECHNIQUES.md). Treat them as starting points, not recipes.

| Slug | Public deep-dive | Template reference |
|---|---|---|
| `career-cv` | <https://koica-tiu.halla.ai/hackathon/samples/career-cv> | Complete branch: `example/career-cv` |
| `agent-triage` | <https://koica-tiu.halla.ai/hackathon/samples/agent-triage> | `src/techniques/agent_orchestration/` |
| `semantic-recommender` | <https://koica-tiu.halla.ai/hackathon/samples/semantic-recommender> | `src/techniques/embeddings_search/` |
| `vision-reader` | <https://koica-tiu.halla.ai/hackathon/samples/vision-reader> | `src/techniques/vision_multimodal/` |
| `streaming-chat` | <https://koica-tiu.halla.ai/hackathon/samples/streaming-chat> | `src/techniques/streaming/` |
| `evaluation-harness` | <https://koica-tiu.halla.ai/hackathon/samples/evaluation-harness> | `src/techniques/evaluation_harness/` |

## 1. CV Feedback Bot

- User: students preparing internship or scholarship applications.
- Problem: CV feedback is slow, inconsistent, and often too generic.
- Demo: paste a synthetic CV and receive structured strengths, weaknesses, suggestions, and privacy flags.
- Technique: JSON-mode structured output.
- Azure: `gpt-4o-mini` chat completion.
- Starting point: use the complete `example/career-cv` branch when you want a full deployment reference.
- Your version could: adapt the rubric to a specific internship track or compare a CV with a job description.

## 2. Multi-step Service Triage Agent

- User: students who need help during the hackathon.
- Problem: tutors receive repeated questions, but some issues need escalation.
- Demo: ask a schedule, submission, cost, or account question and show the selected tool result.
- Technique: agent orchestration and tool calls.
- Azure: `gpt-4o-mini` tool calling; local mock fallback in `src/techniques/agent_orchestration/`.
- Starting point: run `python src/techniques/agent_orchestration/example.py`.
- Your version could: add a team-state store, a tutor queue, or a confidence threshold before escalation.

## 3. Skill-Matched Recommender

- User: students choosing a role, project, or learning path.
- Problem: keyword search misses related skills and goals.
- Demo: enter a student profile and return the top matching roles or project ideas with evidence.
- Technique: embeddings and vector ranking.
- Azure: local cosine search by default; Azure embeddings only if tutors enable a shared deployment.
- Starting point: run `python src/techniques/embeddings_search/example.py`.
- Your version could: combine semantic scores with explicit tags such as Python, design, data, or presentation.

## 4. Document Vision Reader

- User: students or staff extracting information from a screenshot, form, or poster.
- Problem: copying fields manually is slow and error-prone.
- Demo: provide a sample image path and return structured JSON with missing fields.
- Technique: multimodal image input to structured extraction.
- Azure: `gpt-4o-mini` vision path; no Azure AI Vision resource required by default.
- Starting point: run `python src/techniques/vision_multimodal/example.py`.
- Your version could: add a confirmation screen before any extracted field is saved.

## 5. Real-time Streaming Chat

- User: students practicing interviews, presentations, or tutor Q&A.
- Problem: full-response latency makes the demo feel stalled.
- Demo: stream a short answer token by token and show a stable output panel.
- Technique: streaming chat completion.
- Azure: `gpt-4o-mini` streaming; local async stream fallback in `src/techniques/streaming/`.
- Starting point: run `python src/techniques/streaming/example.py`.
- Your version could: add a stop button, final-answer save, or streaming progress indicator.

## 6. Evaluation Harness

- User: teams improving prompt quality before judging.
- Problem: teams rely on one good demo question and do not test failures.
- Demo: score an answer against a rubric and print issues plus the next test to run.
- Technique: evaluation pipeline and LLM-as-judge pattern.
- Azure: deterministic local rubric by default; optional `gpt-4o-mini` JSON judge.
- Starting point: run `python src/techniques/evaluation_harness/example.py`.
- Your version could: add five test cases covering easy, hard, refusal, safety, and cost-sensitive prompts.

## Selection Rule

Pick the idea that can show a working screen in one day. A small complete demo is better than a broad concept without a real user flow.

## MVP Rule

For any idea, the minimum viable demo is:

1. One input screen or form.
2. One visible model or local technique result.
3. One explanation of the Azure technique used or deferred.
4. One safety sentence explaining what the system cannot do.
5. One backup screenshot in case the live demo fails.
