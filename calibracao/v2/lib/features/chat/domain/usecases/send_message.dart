import 'package:fpdart/fpdart.dart';

import '../../../../core/failures.dart';
import '../entities/chat_error.dart';
import '../entities/message.dart';
import '../repositories/chat_repository.dart';

class SendMessage {
  const SendMessage(this._repo);

  final ChatRepository _repo;

  Future<Either<Failure, Message>> call(String text) async {
    if (text.trim().isEmpty) {
      return left(const ChatNetworkError('empty'));
    }
    return _repo.send(text);
  }
}
