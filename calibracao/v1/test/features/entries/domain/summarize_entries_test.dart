import 'package:cal_app/features/entries/domain/entities/entry.dart';
import 'package:cal_app/features/entries/domain/usecases/summarize_entries.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  final summarize = SummarizeEntries();

  group('SummarizeEntries', () {
    test('empty list returns zeros', () {
      final s = summarize(const []);
      expect(s.total, 0);
      expect(s.average, 0);
    });

    test('averages media durations to one decimal', () {
      final s = summarize(const [
        Entry(id: '1', content: 'a', source: 'audio', durationSeconds: 10),
        Entry(id: '2', content: 'b', source: 'audio', durationSeconds: 15),
      ]);
      expect(s.average, 12.5);
    });
  });
}
