# Technique Showcase

This repository has one minimal FastAPI app and five standalone technique scaffolds. Start with the main app for clone-and-run, then open the scaffold that matches your project idea.

## Technique Scaffolds

| Public sample | Template path | What it practices | Azure status |
|---|---|---|---|
| [Multi-step Service Triage Agent](https://koica-tiu.halla.ai/hackathon/samples/agent-triage) | [`src/techniques/agent_orchestration/`](../src/techniques/agent_orchestration/) | Tool calls, state, escalation | Allowed now with `gpt-4o-mini` |
| [Skill-Matched Recommender](https://koica-tiu.halla.ai/hackathon/samples/semantic-recommender) | [`src/techniques/embeddings_search/`](../src/techniques/embeddings_search/) | Embeddings, local vector ranking | Local now, Azure embeddings by tutor approval |
| [Document Vision Reader](https://koica-tiu.halla.ai/hackathon/samples/vision-reader) | [`src/techniques/vision_multimodal/`](../src/techniques/vision_multimodal/) | Image input to structured JSON | Allowed now with `gpt-4o-mini` vision |
| [Real-time Streaming Chat](https://koica-tiu.halla.ai/hackathon/samples/streaming-chat) | [`src/techniques/streaming/`](../src/techniques/streaming/) | Token streaming and UI responsiveness | Allowed now with `gpt-4o-mini` |
| [Evaluation Harness](https://koica-tiu.halla.ai/hackathon/samples/evaluation-harness) | [`src/techniques/evaluation_harness/`](../src/techniques/evaluation_harness/) | Rubrics, test cases, LLM-as-judge | Allowed now with `gpt-4o-mini` |

Each folder has a `README.md`, `example.py`, and `requirements-extra.txt`. Every `example.py` runs without Azure credentials, so teams can build and test UI behavior before spending quota.

## Complete Deployment Anchor

The complete working reference is still the Career CV example:

- Public sample: <https://koica-tiu.halla.ai/hackathon/samples/career-cv>
- Branch: <https://github.com/halla-ai/hackathon-sample-2026/tree/example/career-cv>
- Walkthrough: <https://koica-tiu.halla.ai/hackathon/walkthrough>

Use this branch when you need to see one full path from local code to Azure Container Apps.

## Deferred Voice Note

The bilingual voice assistant idea is not included as a runnable scaffold for this hackathon version. Azure checks on May 25, 2026 found that Azure OpenAI Whisper and TTS were not usable in the current Korea Central OpenAI resource. Azure AI Speech may be provisioned later with tutor/admin approval, but it is not a default student dependency.

## How To Choose

- Choose `agent_orchestration` when the assistant must decide an action.
- Choose `embeddings_search` when the user describes skills, goals, or needs.
- Choose `vision_multimodal` when the input is a screenshot, form, or photo.
- Choose `streaming` when response speed and perceived progress matter.
- Choose `evaluation_harness` when you need evidence that a prompt change improved quality.
