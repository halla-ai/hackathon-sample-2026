# Hackathon Day Guide

Use this file as the team's operating checklist on June 20.

> See also: <https://koica-tiu.halla.ai/hackathon/d-day> (student first-30-minute path + tutor hot-paths) ·
> <https://koica-tiu.halla.ai/hackathon/judging> (rubric) ·
> <https://koica-tiu.halla.ai/hackathon/submission> (slide + README templates)

## First 30 Minutes

1. Sit with your assigned team and confirm the tutor name.
2. Create a repository from this template or open the team's existing repository.
3. Run the sample in mock mode before adding Azure credentials.
4. Sign in with the assigned KOICA-TIU Azure account.
5. Complete MFA if prompted.
6. Add Azure endpoint, deployment, and key to `.env` only after the tutor confirms the team scope.
7. Run one short model call and save one backup screenshot.

### First-30-minute exit criteria

Show your tutor these four items before moving into full build mode:

- The local app opens at `http://127.0.0.1:8000`.
- `/health` returns `{"status":"ok"}`.
- One mock-mode answer is visible in the UI.
- The team can explain one target user and one prepared demo question.

If any item is missing, keep working in mock mode and do not spend Azure tokens yet.

## Team Roles

| Role | Responsibility |
|---|---|
| PM/domain lead | Defines the user, problem, demo story, and final slides. |
| Prompt/data lead | Prepares the context, prompt, test questions, and safety checks. |
| Foundry/backend lead | Connects Azure OpenAI or Foundry and keeps `.env` out of Git. |
| Frontend/demo lead | Builds the visible flow, screenshots, and backup demo path. |

## Tutor Checkpoints

| Time | What the team shows | Tutor decision |
|---|---|---|
| T+30 min | mock-mode UI, `/health`, one target user, one demo question | approve Azure connection or keep mock mode |
| Midpoint | one working API/UI flow, prompt draft, two test questions | reduce scope or approve polish |
| Demo prep | 3-minute script, backup screenshot/video, no secrets on screen | approve final presentation |

Students should not wait silently when blocked. If a checkpoint is at risk, show the current error to the tutor immediately.

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

## Final 10 Minutes

Before presentations begin:

- Close any scripts that repeatedly call Azure.
- Save one final screenshot or short screen recording.
- Confirm the App Service URL or local backup route.
- Hide `.env`, Azure portal keys, and browser tabs containing secrets.
- Put the 5-slide deck and demo URL in one easy-to-open place.
