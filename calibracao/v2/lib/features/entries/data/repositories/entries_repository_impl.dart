import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../../domain/entities/entry.dart';
import '../../domain/repositories/entries_repository.dart';

class EntriesRepositoryImpl implements EntriesRepository {
  final List<Entry> _store = [];

  @override
  Future<Either<Failure, Entry>> create(Entry entry) async {
    _store.add(entry);
    return right(entry);
  }

  @override
  Future<Either<Failure, List<Entry>>> list() async => right(List.of(_store));
}
