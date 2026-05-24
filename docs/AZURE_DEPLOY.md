# Azure Setup And Deployment

## Local Azure AI Foundry Setup

1. Confirm your tutor assigned a team name and quota.
2. Create or use the assigned Azure AI Foundry project.
3. Deploy the assigned chat model.
4. Copy endpoint, key, deployment name, and API version into `.env`.
5. Run `uvicorn src.main:app --reload` and test `/health`.

## Environment Variables

```bash
AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com/
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_DEPLOYMENT=<deployment-name>
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

Do not commit `.env`.

## Azure App Service Deployment Checklist

1. Confirm the team has App Service permission.
2. Set App Service startup command:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

3. Add the same environment variables in App Service configuration.
4. Open `/health` after deployment.
5. Test one normal question and one edge-case question.

## Demo Readiness

- The app starts from a clean checkout.
- `/health` returns `{"status":"ok"}`.
- The UI does not expose secrets.
- The team can explain which Azure service is used.
- The demo has at least three prepared test questions.
