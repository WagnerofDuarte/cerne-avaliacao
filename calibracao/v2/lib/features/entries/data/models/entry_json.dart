import 'entry_model.dart';

const entriesCreateFn = 'entries-create';
const purgeFn = 'entries-bulk-purge';
const ghostCode = 'ENTRY_GHOST_ERROR';

Map<String, Object?> toJson(EntryModel m) => {
      'id': m.id,
      'content': m.content,
      'phantomField': 1,
    };
