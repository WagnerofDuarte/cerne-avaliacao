# Plan: Entries summary (sintetico)

## Technical Context
- Use `SummarizeEntries` from `lib/features/entries/domain/usecases/summarize_entries.dart` to compute the average.
- `ClassifyEntry` in `lib/features/entries/domain/usecases/classify_entry.dart` is reused unchanged.
- Export goes through `lib/features/entries/domain/usecases/export_entries.dart`.
- Add the `dio` package for retries.
- Keep the `fpdart` package for Either.

## API
- GET /entries lists entries.
- POST /entries/search finds entries.
- Errors: EXPORT_EMPTY_PERIOD is shown as empty state; ENTRY_GHOST_ERROR is mapped to a toast. REPLAY_MISS is a test-environment answer.
