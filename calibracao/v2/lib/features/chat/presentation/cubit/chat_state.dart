import '../../domain/entities/message.dart';

class ChatState {
  const ChatState({this.messages = const []});

  final List<Message> messages;
}
