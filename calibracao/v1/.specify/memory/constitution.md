# Constitution (sintetica, calibracao)

## Principles
- Use `flutter_bloc` for state management and keep Clean Architecture in three layers.
- Use the `dio` package for HTTP; the client lives in `lib/core/network/api_client.dart`.
- `EntriesRepositoryImpl` implements `EntriesRepository` and lives in `lib/features/entries/data/repositories/`.
- `ChatCubit` must never import `EntriesRepositoryImpl`; chats create entries through `EntryCreator` only.
- Entries are always sorted newest first inside `BuildTimeline` (`lib/features/timeline/domain/usecases/build_timeline.dart`).
- Tests should be written first.
- Document every decision in `docs/decisions.md`.
