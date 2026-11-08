import 'package:cal_app/features/entries/domain/entities/entry.dart';
import 'package:cal_app/features/entries/domain/usecases/validate_entry.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('ValidateEntry', () {
    test('runs on a titled entry', () {
      ValidateEntry()(const Entry(id: '1', content: 'c', source: 'manual', title: 't'));
    });
  });
}
