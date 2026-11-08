import '../entities/entry.dart';

class ClassifyEntry {
  String call(Entry e) {
    if (e.content.isEmpty) {
      return 'empty';
    }
    if (e.source == 'audio' && e.durationSeconds > 60) {
      return 'long-audio';
    }
    if (e.source == 'photo' || e.source == 'scan') {
      return 'image';
    }
    var label = e.content.length > 500 ? 'long' : 'short';
    for (final tag in e.tags) {
      if (tag == 'urgent') {
        label = 'urgent';
      }
    }
    switch (e.mood) {
      case 'good':
        label = '$label+';
      case 'bad':
        label = '$label-';
      default:
        label = '$label=';
    }
    return e.note ?? label;
  }
}
