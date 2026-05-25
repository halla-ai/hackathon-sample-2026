# Embeddings Search

## What this demonstrates

A small semantic recommender that ranks short texts with local cosine search and can optionally switch to Azure embeddings.

## Why your hackathon project might want it

Use this when users describe skills, goals, or needs in their own words and exact keyword filters are too rigid. It maps to the embeddings and retrieval curriculum without requiring Azure AI Search during the event.

## Run it locally

```bash
cd src/techniques/embeddings_search
python example.py
```

The default path is local and deterministic. To test Azure embeddings later, set `USE_AZURE_EMBEDDINGS=1` and `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`.

## Read it line-by-line

The example tokenizes a query, builds small vectors, computes cosine similarity, and prints the top matches. The optional Azure path uses the same ranking shape with model-generated embeddings.

## Extend it

- How would your version combine skill tags with semantic similarity?
- What source fields should be shown so users trust the recommendation?
- How would you update the corpus without re-ranking everything manually?
- What threshold should trigger "no good match yet"?

## Watch out for

- Symptom: every result looks relevant. Cause: corpus items are too similar. Fix: add clearer labels and examples.
- Symptom: rankings are hard to explain. Cause: only dense scores are shown. Fix: display matched tags or evidence.
- Symptom: cost rises unexpectedly. Cause: re-embedding the full corpus every request. Fix: cache corpus vectors.

## Where to go next

- Public deep dive: https://koica-tiu.halla.ai/hackathon/samples/semantic-recommender
- Technique catalog: ../../../../docs/TECHNIQUES.md
- Microsoft Learn: https://learn.microsoft.com/azure/ai-foundry/openai/tutorials/embeddings
