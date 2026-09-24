# P-RF10 — Save a chat message as an entry

Let the user turn one of their own chat messages into a journal entry.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF10.
- Prototype state: "Tela 1 — Bookmark", with its sub-states (prototype extract, section 2.2).
- Backend: `POST /entries` with `source` `chat` and `chatMessageId`.
- Depends on: RF01, RF04.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
