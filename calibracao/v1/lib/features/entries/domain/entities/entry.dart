class Entry {
  const Entry({
    required this.id,
    required this.content,
    required this.source,
    this.durationSeconds = 0,
    this.tags = const [],
    this.mood = '',
    this.note,
    this.title = '',
  });

  final String id;
  final String content;
  final String source;
  final int durationSeconds;
  final List<String> tags;
  final String mood;
  final String? note;
  final String title;

  bool get isMedia => source == 'audio' || source == 'photo';
}
