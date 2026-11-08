import 'package:cal_app/features/entries/domain/entities/entry.dart';
import 'package:cal_app/features/entries/domain/usecases/classify_entry.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  final classify = ClassifyEntry();

  group('ClassifyEntry', () {
    test('empty content is empty', () {
      expect(classify(const Entry(id: '1', content: '', source: 'manual')), 'empty');
    });

    test('audio over a minute is long-audio', () {
      const e = Entry(id: '2', content: 'x', source: 'audio', durationSeconds: 61);
      expect(classify(e), 'long-audio');
    });

    test('photo is image', () {
      expect(classify(const Entry(id: '3', content: 'x', source: 'photo')), 'image');
    });

    test('urgent tag wins over length', () {
      const e = Entry(id: '4', content: 'x', source: 'manual', tags: ['urgent']);
      expect(classify(e), 'urgent=');
    });

    test('good mood appends plus', () {
      const e = Entry(id: '5', content: 'x', source: 'manual', mood: 'good');
      expect(classify(e), 'short+');
    });
  });
}
