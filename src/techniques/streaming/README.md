# Streaming

## What this demonstrates

An async token stream that prints partial output as it arrives.

## Why your hackathon project might want it

Use this for tutor chat, interview practice, live coding help, or any flow where waiting for the full answer makes the demo feel slow. It extends the basic chat-completion lesson without adding another Azure service.

## Run it locally

```bash
cd src/techniques/streaming
python example.py
```

No Azure credentials are required; the local stream prints deterministic chunks.

## Read it line-by-line

The example exposes the same async iterator shape for mock and Azure modes. A web app can connect this pattern to server-sent events or a websocket.

## Extend it

- How would your UI show a stop button while streaming?
- What should be streamed to the user, and what should stay server-side?
- How would you save only the final answer after the stream ends?
- How would you handle a network interruption halfway through?

## Watch out for

- Symptom: the UI flashes or reflows. Cause: appending text without stable layout. Fix: reserve the answer panel height.
- Symptom: private tool output appears. Cause: streaming internal state. Fix: stream final answer tokens only.
- Symptom: tests are flaky. Cause: timing-based assertions. Fix: test collected chunks, not exact delays.

## Where to go next

- Public deep dive: https://koica-tiu.halla.ai/hackathon/samples/streaming-chat
- Technique catalog: ../../../../docs/TECHNIQUES.md
- Microsoft Learn: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/chatgpt
