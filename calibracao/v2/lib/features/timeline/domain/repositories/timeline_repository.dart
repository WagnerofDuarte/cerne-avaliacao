import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../entities/timeline_item.dart';

abstract class TimelineRepository {
  Future<Either<Failure, List<TimelineItem>>> load();
}
