# P-RF07 — Multi-source history (timeline)

Show all the user's entries in a timeline, whatever their origin, with a per-entry synchronization badge.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF07.
- Prototype states: "Tela 4 — Meus Registros" (default) and "Tela 4 — Vazio" (prototype extract, section 2.4); the "Sessão expirada" overlay (section 4).
- Badge semantics: `docs/input/backend/sync-badge.md`.
- Backend: `GET /entries`, `GET /entries/:id`, `GET /auth/session`, `POST /auth/refresh`.
- Depends on: F000, RF01.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
