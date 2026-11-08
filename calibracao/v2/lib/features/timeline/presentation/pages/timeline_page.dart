import 'package:flutter/material.dart';

import '../../../../core/design_tokens.dart';

class TimelinePage extends StatelessWidget {
  const TimelinePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(AppSpacing.sm),
      child: Text(
        'Linha do tempo',
        style: TextStyle(
          fontSize: AppTypography.body,
          fontFamily: AppTypography.fontFamily,
        ),
      ),
    );
  }
}
