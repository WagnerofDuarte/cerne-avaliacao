import '../../domain/entities/message.dart';

class ChatMessageModel {
  const ChatMessageModel(this.author, this.text);

  final String author;
  final String text;

  Message toEntity() => Message(author, text);
}
