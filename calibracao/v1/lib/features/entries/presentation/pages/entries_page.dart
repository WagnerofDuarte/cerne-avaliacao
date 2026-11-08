import 'package:flutter/material.dart';

import '../../../../core/design_tokens.dart';

// Comentario com literal que nao conta: Color(0xFF000000), fontSize: 99
class EntriesPage extends StatelessWidget {
  const EntriesPage({super.key});

  @override
  Widget build(BuildContext context) {
    const label = 'fontSize: 12 e Color(0xFF111111) dentro de string nao contam';
    return Container(
      color: const Color(0xFFAA3366),
      padding: const EdgeInsets.all(13),
      child: Column(
        children: [
          const SizedBox(height: AppSpacing.md),
          Text(
            'Meus Registros',
            style: TextStyle(
              fontSize: 17,
              fontFamily: 'Courier',
              color: AppColors.primary,
            ),
          ),
          const Text(
            label,
            style: TextStyle(
              fontSize: AppTypography.body,
              fontFamily: AppTypography.fontFamily,
            ),
          ),
        ],
      ),
    );
  }
}
