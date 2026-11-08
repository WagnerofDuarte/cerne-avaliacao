import '../entities/entry.dart';

class ValidateEntry {
  bool call(Entry e) {
    return e.title.trim().isNotEmpty && e.title.length <= 80;
  }
}
