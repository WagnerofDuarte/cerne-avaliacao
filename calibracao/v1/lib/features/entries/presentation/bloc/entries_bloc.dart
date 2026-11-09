import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/repositories/entries_repository.dart';
import 'entries_event.dart';
import 'entries_state.dart';

class EntriesBloc extends Bloc<EntriesEvent, EntriesState> {
  EntriesBloc(this._repository) : super(const EntriesState()) {
    on<EntriesRequested>((event, emit) async {
      final result = await _repository.list();
      result.fold((_) {}, (items) => emit(EntriesState(items: items)));
    });
  }

  final EntriesRepository _repository;
}
