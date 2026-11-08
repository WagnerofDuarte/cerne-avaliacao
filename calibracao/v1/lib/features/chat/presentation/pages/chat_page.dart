import 'package:flutter/material.dart';

import '../../../../core/design_tokens.dart';

class ChatPage extends StatelessWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.all(AppSpacing.md),
      child: Text(
        'Conversa',
        style: TextStyle(
          fontSize: AppTypography.title,
          fontFamily: AppTypography.fontFamily,
        ),
      ),
    );
  }
}
