# Project Ideas

## 1. Campus FAQ RAG

- User: first-year TIU students
- Problem: students repeatedly ask about classes, campus rules, and schedules
- Demo: upload a small FAQ file, ask questions, answer with source titles
- Azure: AI Foundry project, Azure OpenAI chat deployment
- Extension: add multilingual Korean/Uzbek/English answer mode

## 2. Internship Matching Assistant

- User: AI department students preparing for internships
- Problem: students do not know which role fits their skills
- Demo: paste a profile, receive role suggestions and learning gaps
- Azure: Azure OpenAI prompt flow
- Extension: add CV rewrite suggestions

## 3. Public Service Explainer

- User: citizens reading public notices
- Problem: official notices are difficult to understand
- Demo: summarize a notice into plain language and action checklist
- Azure: Azure OpenAI, content safety review
- Extension: add risk labels for uncertain parts

## 4. Tashkent Tourism Planner

- User: exchange students or visitors
- Problem: planning a short trip requires local context
- Demo: create a half-day itinerary based on time, budget, and interests
- Azure: Azure OpenAI chat
- Extension: connect a simple places dataset

## 5. Business Brief Generator

- User: student startup teams
- Problem: teams need quick market and customer summaries
- Demo: generate a one-page business brief from a product idea
- Azure: Azure OpenAI, prompt templates
- Extension: add evaluation checklist for feasibility

## 6. Real Estate Assistant

- User: students looking for housing
- Problem: listings are hard to compare
- Demo: convert listing text into pros, cons, questions, and red flags
- Azure: Azure OpenAI
- Extension: add monthly budget calculator

## Selection Rule

Pick the idea that can show a working screen in one day. A small complete demo
is better than a broad concept without a real user flow.

## MVP Rule

For any idea, the minimum viable demo is:

1. One input screen or form.
2. One Azure OpenAI or Foundry model call.
3. One visible result that helps the target user decide or act.
4. One safety sentence explaining what the system cannot do.
5. One backup screenshot in case the live demo fails.

## Fast Variations

| Base idea | Easy variation | Harder variation |
|---|---|---|
| Campus FAQ RAG | Ask questions from one FAQ file | Add multilingual answers with source titles |
| Internship Matching | Compare one profile to three roles | Add ranking explanation and skill-gap plan |
| Public Service Explainer | Rewrite one notice into plain language | Add uncertainty labels and next-step checklist |
| Tourism Planner | Plan a half-day itinerary | Add budget and accessibility constraints |
| Business Brief | Generate a one-page brief | Add risk scoring and pitch outline |
| Real Estate Assistant | Compare two listings | Add red-flag detection and budget calculator |
