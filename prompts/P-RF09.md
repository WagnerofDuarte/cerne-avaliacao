# P-RF09 — Temporal summaries / dashboard

Build the Settings screen with the evolution dashboard, and the profile and account actions that live on it.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF09; RNF05 (section 4) for account deletion.
- Prototype states: "Tela 6 — Configurações" in its four dashboard variations and "Tela 6 — Confirmar exclusão de conta" (prototype extract, section 2.6); profile name editing, "Sair" and "Apagar conta".
- Backend: `GET /dashboard/aggregate`, `GET /dashboard/narrative`, `PATCH /account/settings`, `DELETE /account`, `POST /auth/logout`.
- Depends on: F000, RF01.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
