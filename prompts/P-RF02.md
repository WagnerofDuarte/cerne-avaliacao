# P-RF02 — Speech-to-text / OCR processing

Turn captured audio into text on the device, and photos into text through the backend, before saving the entry.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF02.
- Prototype states: "Áudio — Processando / Transcrito / Erro" and "Foto — Processando OCR / Reconhecido / Erro" (prototype extract, sections 2.3 and 4).
- On-device speech-to-text with `whisper_ggml` (audio never goes to the backend); OCR with `POST /media/ocr`; then `POST /entries`.
- Test material: `docs/input/backend/fixtures/`.
- Depends on: RF01.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
