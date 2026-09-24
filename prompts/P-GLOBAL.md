# P-GLOBAL — Product vision

**Cerne** is a mobile reflective-journaling app with an AI assistant. The user records their day by text, audio or photo; a conversational agent consults those records through semantic search to answer with context and to offer proactive insights. The app also keeps a timeline of all records, lets the user search and filter them, exports a personal summary and shows an evolution dashboard. Access is protected by biometrics or PIN.

## Scope

The functional requirements RF01–RF10 in `docs/input/requirements.md`, section 1:
- RF01 — Multimodal capture (text / audio / photo)
- RF02 — Speech-to-text / OCR processing
- RF03 — Biometric authentication vault
- RF04 — Interactive chat with memory (RAG)
- RF05 — Personal summary export
- RF06 — Semantic search / filter over journal entries
- RF07 — Multi-source history (timeline)
- RF08 — Proactive insights (mechanism)
- RF09 — Temporal summaries / dashboard
- RF10 — Save a chat message as an entry

Plus the quality requirements RNF01–RNF09 (sections 3 and 4) and a foundation unit (F000). Delivery order: section 12.

## Out of scope

The extension features of section 2 (manual tags, action plans, persona): no functional implementation; a menu entry may exist as a placeholder. The backend already exists and is not changed.

## Where everything is

- `docs/input/requirements.md` — requirements, screens, endpoints, delivery order, technical constraints.
- `docs/input/prototype/` — the visual prototype (`cerne-prototype.html`) and its extract.
- `docs/input/backend/` — API contract and backend documentation.

## Do not

- Build extension features.
- Change the backend.
- Add features that are not in `requirements.md`.
