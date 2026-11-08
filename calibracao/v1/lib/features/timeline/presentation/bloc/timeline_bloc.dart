import 'package:flutter_bloc/flutter_bloc.dart';

import '../../../entries/presentation/bloc/entries_bloc.dart';
import '../../domain/repositories/timeline_repository.dart';
import 'timeline_event.dart';
import 'timeline_state.dart';

class TimelineBloc extends Bloc<TimelineEvent, TimelineState> {
  TimelineBloc(this._repository, this._entriesBloc)
      : super(const TimelineState()) {
    on<TimelineRequested>((event, emit) async {
      final result = await _repository.load();
      result.fold((_) {}, (items) => emit(TimelineState(items: items)));
    });
  }

  final TimelineRepository _repository;
  final EntriesBloc _entriesBloc;
}
