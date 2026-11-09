import '../../domain/entities/timeline_item.dart';

class TimelineModel {
  const TimelineModel(this.id, this.label);

  final String id;
  final String label;

  TimelineItem toEntity() => TimelineItem(id, label);
}
