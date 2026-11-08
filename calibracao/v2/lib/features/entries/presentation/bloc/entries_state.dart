import '../../domain/entities/entry.dart';

class EntriesState {
  const EntriesState({this.items = const []});

  final List<Entry> items;
}
