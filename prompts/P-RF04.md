# P-RF04 — Interactive chat with memory (RAG)

Build the conversation with the AI agent, which answers with context from the user's previous entries.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF04.
- Prototype states: "Tela 1 — Home/Chat" (default), "Streaming", "Falha ao gerar resposta", "Offline"; "Tela 3 — Menu lateral" with the session list and the new-conversation action (prototype extract, sections 2.2 and 4).
- Backend: `POST /chat/sessions`, `GET /chat/sessions`, `GET /chat/sessions/:id/messages`, `POST /chat/sessions/:id/messages` (SSE), `POST /chat/sessions/:id/messages/:userMessageId/retry` (requirements, section 6.3).
- Depends on: F000, RF03.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
