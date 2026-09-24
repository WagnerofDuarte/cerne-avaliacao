# P-RF01 — Multimodal capture

Let the user create a journal entry by text, audio recording or photo, from the Insertion Modal.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF01.
- Prototype states: Insertion modal — "Texto", "Áudio — Gravando", "Foto — Captura" (prototype extract, section 2.3); opened by the "+" button of Home/Chat.
- Backend: `POST /entries` with `source` `manual`/`audio`/`photo`.
- Depends on: F000, RF03.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
