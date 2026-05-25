# Vision Multimodal

## What this demonstrates

A document-image reader that turns an image into structured JSON, with a deterministic mock fallback.

## Why your hackathon project might want it

Use this when the user has a screenshot, form photo, poster, or handwritten note and text-only input would be awkward. It maps to the multimodal curriculum and uses the currently verified `gpt-4o-mini` vision path.

## Run it locally

```bash
cd src/techniques/vision_multimodal
python example.py
python example.py path/to/your-image.png
```

Without Azure credentials, both commands return the same mock extraction shape.

## Read it line-by-line

The script accepts an image path, builds a data URI only when Azure is configured, asks for JSON output, and otherwise returns a stable local result for UI development.

## Extend it

- What fields would your target user need from the image?
- How would you ask for confirmation before saving extracted data?
- What images are unsafe or private and should be rejected?
- How would you compare model extraction against a hand-labeled answer?

## Watch out for

- Symptom: the image fails to parse. Cause: invalid image bytes or unsupported format. Fix: test with a small PNG first.
- Symptom: JSON fields change between runs. Cause: loose prompt. Fix: name exact fields and use JSON mode.
- Symptom: private IDs appear in output. Cause: unsafe source image. Fix: use public or synthetic examples.

## Where to go next

- Public deep dive: https://koica-tiu.halla.ai/hackathon/samples/vision-reader
- Technology matrix: https://koica-tiu.halla.ai/hackathon/technology
- Microsoft Learn: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/gpt-with-vision
