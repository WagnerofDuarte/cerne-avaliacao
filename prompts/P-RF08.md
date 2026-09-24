# P-RF08 — Proactive insights (mechanism)

Insert an AI suggestion into the chat without the user asking for it.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF08; parameter: section 10.
- Prototype state: "Tela 1 — Insight" (prototype extract, section 2.2).
- Backend: `POST /chat/sessions/:id/insight`.
- Depends on: RF04.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
