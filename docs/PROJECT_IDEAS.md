# Project Ideas

Each track below has a deep-dive page on the public site with full architecture,
prompt pack, code snippet, demo screens, Azure budget estimate, and pitfalls:

| Track | Public deep-dive |
|---|---|
| Campus FAQ RAG | <https://koica-tiu.halla.ai/hackathon/samples/education-faq> |
| Internship / CV | <https://koica-tiu.halla.ai/hackathon/samples/career-cv> |
| Public Service | <https://koica-tiu.halla.ai/hackathon/samples/public-service> |
| Tourism Planner | <https://koica-tiu.halla.ai/hackathon/samples/tourism> |
| Business Brief | <https://koica-tiu.halla.ai/hackathon/samples/business> |
| Real Estate | <https://koica-tiu.halla.ai/hackathon/samples/realestate> |

Read the deep-dive before you start coding — it tells you which Azure services
to use, what the architecture should look like, and the common pitfalls.

## 1. Campus FAQ RAG

- User: first-year TIU students
- Problem: students repeatedly ask about classes, campus rules, and schedules
- Demo: upload a small FAQ file, ask questions, answer with source titles
- Azure: AI Foundry project, Azure OpenAI chat deployment
- Starter data: 10-20 public FAQ rows about class times, campus rules, rooms, and contacts
- First demo question: "Where can a first-year student ask about course registration?"
- Minimum screen: one question box, one answer panel, and one source-title list
- Safety note: answer only from the FAQ; if the answer is missing, say which office to contact
- Extension: add Uzbek/English answer mode

## 2. Internship Matching Assistant

- User: AI department students preparing for internships
- Problem: students do not know which role fits their skills
- Demo: paste a profile, receive role suggestions and learning gaps
- Azure: Azure OpenAI prompt flow
- Starter data: three sample job descriptions and one synthetic student profile
- First demo question: "Which internship role fits this profile best, and what should I learn next?"
- Minimum screen: profile input, role recommendation, skill-gap checklist
- Safety note: do not collect passport numbers, phone numbers, addresses, or private grades
- Extension: add CV rewrite suggestions

## 3. Public Service Explainer

- User: citizens reading public notices
- Problem: official notices are difficult to understand
- Demo: summarize a notice into plain language and action checklist
- Azure: Azure OpenAI, content safety review
- Starter data: one public notice copied into a text file with title and source URL
- First demo question: "Explain this notice in plain English and list what the citizen should do."
- Minimum screen: notice input, plain-language summary, action checklist
- Safety note: do not provide legal advice; direct users to the official office for final answers
- Extension: add risk labels for uncertain parts

## 4. Tashkent Tourism Planner

- User: exchange students or visitors
- Problem: planning a short trip requires local context
- Demo: create a half-day itinerary based on time, budget, and interests
- Azure: Azure OpenAI chat
- Starter data: 8-12 public place descriptions with opening hours and approximate travel notes
- First demo question: "Plan a 4-hour low-budget route near central Tashkent for two students."
- Minimum screen: preferences form, itinerary, budget estimate, fallback plan
- Safety note: mark travel times as estimates and avoid unsafe or unverified recommendations
- Extension: connect a simple places dataset

## 5. Business Brief Generator

- User: student startup teams
- Problem: teams need quick market and customer summaries
- Demo: generate a one-page business brief from a product idea
- Azure: Azure OpenAI, prompt templates
- Starter data: product idea, target customer, price assumption, and three competitor notes
- First demo question: "Turn this startup idea into a one-page business brief for judges."
- Minimum screen: idea form, customer segment, value proposition, risk list
- Safety note: label all market numbers as assumptions unless a source is provided
- Extension: add evaluation checklist for feasibility

## 6. Real Estate Assistant

- User: students looking for housing
- Problem: listings are hard to compare
- Demo: convert listing text into pros, cons, questions, and red flags
- Azure: Azure OpenAI
- Starter data: two synthetic housing listings with rent, location, and conditions
- First demo question: "Compare these two listings and list questions I should ask before visiting."
- Minimum screen: listing input, comparison table, red flags, follow-up questions
- Safety note: do not rank neighborhoods by sensitive attributes or invent unavailable listing details
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
