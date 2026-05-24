# Hackathon Day Guide

Use this file as the team's operating checklist on June 20.

## First 30 Minutes

1. Sit with your assigned team and confirm the tutor name.
2. Create a repository from this template or open the team's existing repository.
3. Run the sample in mock mode before adding Azure credentials.
4. Sign in with the assigned KOICA-TIU Azure account.
5. Complete MFA if prompted.
6. Add Azure endpoint, deployment, and key to `.env` only after the tutor confirms the team scope.
7. Run one short model call and save one backup screenshot.

## Team Roles

| Role | Responsibility |
|---|---|
| PM/domain lead | Defines the user, problem, demo story, and final slides. |
| Prompt/data lead | Prepares the context, prompt, test questions, and safety checks. |
| Foundry/backend lead | Connects Azure OpenAI or Foundry and keeps `.env` out of Git. |
| Frontend/demo lead | Builds the visible flow, screenshots, and backup demo path. |

## Submission Checklist

- README explains the problem, user, Azure resources, and demo flow.
- `.env.example` is committed, `.env` is not committed.
- The app works in mock mode and, if assigned credentials are available, Azure mode.
- The 3-minute demo has a backup screenshot or recording.
- The 5-slide deck explains problem, user, Azure workflow, result, and limitation.
- No private personal data, API keys, passwords, or hidden prompts appear in the repo or slides.

## When Something Fails

| Symptom | Team action | Tutor action |
|---|---|---|
| Azure sign-in fails | Keep working in mock mode. | Check assigned account and escalate to admin. |
| MFA blocks progress | Stop retrying and show the screen. | Request reset or verification from operations. |
| Foundry project is missing | Confirm team number and project name. | Check admin dashboard assignment. |
| Model call fails | Check `.env`, deployment name, endpoint, and API version. | Verify the assigned deployment and quota status. |
| Token use spikes | Stop repeated tests and shorten prompts. | Review loops, max tokens, and background calls. |
| App deployment fails | Prepare local demo and screenshots. | Check the assigned App Service slot. |

## Demo Script

1. Our user is ...
2. The problem is ...
3. Our prototype helps by ...
4. We used Azure/Foundry for ...
5. The demo result is ...
6. The limitation and next step are ...
