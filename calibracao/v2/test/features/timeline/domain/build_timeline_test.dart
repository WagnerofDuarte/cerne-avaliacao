import 'package:cal_app/features/entries/domain/entities/entry.dart';
import 'package:cal_app/features/timeline/domain/usecases/build_timeline.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const entries = [
    Entry(id: 'a', content: 'one', source: 'manual'),
    Entry(id: 'b', content: 'two', source: 'manual'),
  ];

  group('BuildTimeline', () {
    test('newest first reverses', () {
      final ids = BuildTimeline()(entries).map((i) => i.id).toList();
      expect(ids, ['end', 'b', 'a']);
    });
  });
}
