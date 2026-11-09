import '../../../entries/domain/entities/entry.dart';
import '../entities/timeline_item.dart';

class BuildTimeline {
  List<TimelineItem> call(List<Entry> entries, {bool newestFirst = true}) {
    final items = <TimelineItem>[
      for (final e in entries) TimelineItem(e.id, e.content),
      if (entries.isNotEmpty) const TimelineItem('end', ''),
    ];
    if (newestFirst) {
      return items.reversed.toList();
    }
    return items;
  }
}
