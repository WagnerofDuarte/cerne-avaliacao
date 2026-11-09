import 'package:flutter/material.dart';

import '../../../../core/design_tokens.dart';

class TimelineCard extends StatelessWidget {
  const TimelineCard({super.key, required this.label});

  final String label;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.sm),
      child: Text(label, style: const TextStyle(fontSize: AppTypography.body)),
    );
  }
}
