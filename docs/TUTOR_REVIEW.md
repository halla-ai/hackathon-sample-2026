# Tutor Review Guide

## Review Cadence

| Time | Tutor Action | Output |
|---|---|---|
| Kickoff | approve team problem and scope | one-sentence problem statement |
| Midpoint | check working endpoint and prompt quality | top 3 fixes |
| Demo prep | rehearse 3-minute presentation | demo checklist |
| Final | score prototype and learning outcome | rubric score |

## Team Scope Questions

1. Who is the exact user?
2. What task becomes easier because of AI?
3. What can be shown on screen in three minutes?
4. Which Azure service is used?
5. What data must not be entered into the system?
6. How will the team know the answer is good enough?

## Rubric

| Criterion | Points | Evidence |
|---|---:|---|
| Problem clarity | 20 | target user and concrete pain point |
| Working demo | 25 | live UI/API with stable flow |
| Azure use | 20 | clear use of Foundry/OpenAI/App Service |
| Prompt quality | 15 | grounded, safe, testable prompts |
| Responsible AI | 10 | privacy and hallucination controls |
| Presentation | 10 | concise story and visible result |

## Intervention Rules

- If a team has no running app at midpoint, reduce scope to one API call and one page.
- If a team is spending tokens heavily, lower max tokens and use mock mode for UI work.
- If a team uses private personal data, stop the test and replace it with synthetic data.
- If a team cannot explain its user, make them rewrite the problem statement before coding.
