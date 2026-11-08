import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../entities/message.dart';

abstract class ChatRepository {
  Future<Either<Failure, Message>> send(String text);

  Future<String> lastDraft();
}
