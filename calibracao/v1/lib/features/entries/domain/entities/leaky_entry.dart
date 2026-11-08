import 'package:cal_app/features/entries/data/models/entry_model.dart';

class LeakyEntry {
  const LeakyEntry(this.model);

  final EntryModel? model;

  String describe() => model?.id ?? 'none';
}
