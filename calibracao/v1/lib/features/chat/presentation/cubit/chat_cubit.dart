import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../entries/data/repositories/entries_repository_impl.dart';
import '../../../entries/domain/entities/entry.dart';
import '../../domain/usecases/send_message.dart';
import 'chat_state.dart';

class ChatCubit extends Cubit<ChatState> {
  ChatCubit(this._send, this._entries) : super(const ChatState());

  final SendMessage _send;
  final EntriesRepositoryImpl _entries;

  Future<void> send(String text) async {
    final result = await _send(text);
    result.fold((_) {}, (m) => emit(ChatState(messages: [...state.messages, m])));
  }

  Future<void> save(String text) async {
    await _entries.create(Entry(id: 'c1', content: text, source: 'chat'));
  }
}
