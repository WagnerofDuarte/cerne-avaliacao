import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../../domain/entities/timeline_item.dart';
import '../../domain/repositories/timeline_repository.dart';

class TimelineRepositoryImpl implements TimelineRepository {
  @override
  Future<Either<Failure, List<TimelineItem>>> load() async => right(const []);
}
