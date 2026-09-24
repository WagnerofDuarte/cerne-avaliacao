# P-RF06 — Semantic search / filter

Let the user find entries by meaning and narrow them with filters, on the My Records screen.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF06; parameter: section 10.
- Prototype states: search bar of "Tela 4 — Meus Registros", "Tela 4 — Sheet de filtro", "Tela 4 — Filtros ativos" (prototype extract, section 2.4, including the note on categories).
- Backend: `GET /entries/search`, `GET /entries`.
- Test material: `docs/input/backend/fixtures/seeded-search-entries.md`.
- Depends on: RF07.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
