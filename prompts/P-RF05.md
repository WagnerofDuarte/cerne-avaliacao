# P-RF05 — Personal summary export

Let the user export a narrative summary of their entries as PDF, and always be able to download the raw data.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF05.
- Prototype states: the export sheet — "Pendente", "Processando", "Concluído", "Erro", "Período vazio" (prototype extract, section 2.5); opened by the download icon of Meus Registros.
- Screen ↔ job status mapping: `docs/input/backend/export-screen-states.md`.
- Backend: `POST /export/summary`, `GET /export/:jobId/status`, `GET /export/:jobId/download`.
- Depends on: RF07.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
