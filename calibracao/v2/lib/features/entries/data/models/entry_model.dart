import 'package:flutter/foundation.dart';

import '../../domain/entities/entry.dart';

@immutable
class EntryModel {
  const EntryModel(this.id, this.content);

  final String id;
  final String content;

  Entry toEntity() => Entry(id: id, content: content, source: 'manual');
}
