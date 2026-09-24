# P-SETUP — Project principles

Use the principles below as the governing rules for all work in this repository.

## Product and sources

- This repository builds **Cerne**, a mobile reflective-journaling app with an AI assistant.
- The product input is in `docs/input/`:
  - `requirements.md` — functional and quality requirements, screens, API, delivery order and technical constraints;
  - `prototype/` — the frozen visual prototype and its extract (visual tokens, list of states);
  - `backend/` — documentation of the existing backend: API, error taxonomy, screen-state map, sync-badge semantics and fixtures.
- These documents are the source of truth for the product. Where they are silent, make a reasonable technical decision.

## Fixed technical stack

- Flutter and Dart at the version pinned for this repository (fvm).
- State management: `flutter_bloc`.
- Clean Architecture, three layers per feature.
- Error handling: `fpdart`; repositories return `Either<Failure, T>`.
- Test doubles: `mocktail`.
- On-device speech-to-text: `whisper_ggml`. Audio never goes to the backend.
- Visual tokens: `lib/core/design_tokens.dart` is the single source of colors, typography, spacing and radii.
- Platform: iOS.
- Backend: already built and frozen. The app consumes its API as documented in `docs/input/backend/`. All AI features, including semantic search, are provided by the backend. Configuration and credentials come from a `.env` file at the project root, with exactly two variables: `FUNCTIONS_BASE_URL` and `SUPABASE_ANON_KEY`. Send `SUPABASE_ANON_KEY` as the `Authorization: Bearer <key>` header (and `apikey` header, if your HTTP client needs it) on every call to `{FUNCTIONS_BASE_URL}/<function>` — including before login, since the Edge Functions require it to accept the request at all. After login, keep using the same anon key for Edge Function invocation; the user's own session token is a separate concern, handled by the auth endpoints themselves.
- Everything else — routing, HTTP client, local cache, dependency injection, secure storage, biometrics, charts — is your choice.

## Folder convention

```
lib/
  core/
  features/
    <feature>/
      data/
      domain/
      presentation/
```

## Quality

- Meet the quality requirements RNF01–RNF09 in `docs/input/requirements.md`.
- The domain layer follows RNF06.

## User interface

- The UI is faithful to the prototype in `docs/input/prototype/`.
- UI text is in **Portuguese**, exactly as written in the prototype.
- Code identifiers, comments and project documentation are in English.

## Scope

- Implement the functional requirements in the delivery order given in `docs/input/requirements.md`.
- Extension features (section 2 of `requirements.md`) are not implemented. A menu entry may exist as a placeholder.

## Do not

- Change the backend, its API contract or its configuration.
- Call AI providers directly from the app.
- Write visual values (colors, font sizes, spacing, radii) outside `design_tokens.dart`.
- Implement extension features.
- Commit `.env` or any credential.
- Edit the files in `docs/input/`.
