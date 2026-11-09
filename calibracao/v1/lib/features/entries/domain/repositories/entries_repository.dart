import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../entities/entry.dart';

abstract class EntriesRepository {
  Future<Either<Failure, Entry>> create(Entry entry);

  Future<Either<Failure, List<Entry>>> list();
}
