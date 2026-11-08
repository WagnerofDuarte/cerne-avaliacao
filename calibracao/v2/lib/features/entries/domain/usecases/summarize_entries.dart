import '../entities/entry.dart';

class Summary {
  const Summary(this.total, this.average);

  final int total;
  final double average;
}

class SummarizeEntries {
  Summary call(List<Entry> entries) {
    if (entries.isEmpty) return const Summary(0, 0);
    var total = 0;
    var sum = 0.0;
    for (final e in entries.where((x) => x.content.isNotEmpty && x.isMedia)) {
      total++;
      sum += e.durationSeconds;
    }
    final avg = total == 0 ? 0.0 : sum / total;
    return Summary(total, avg.roundToDouble());
  }
}
