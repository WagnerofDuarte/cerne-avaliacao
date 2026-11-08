import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../../domain/entities/message.dart';
import '../../domain/repositories/chat_repository.dart';

class ChatRepo implements ChatRepository {
  @override
  Future<Either<Failure, Message>> send(String text) async =>
      right(Message('ai', text));

  @override
  Future<String> lastDraft() async => '';
}
