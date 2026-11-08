import '../../domain/entities/timeline_item.dart';

class TimelineState {
  const TimelineState({this.items = const []});

  final List<TimelineItem> items;
}
