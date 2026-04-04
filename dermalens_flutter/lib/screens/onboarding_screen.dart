import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/navigation_provider.dart';

class OnboardingScreen extends ConsumerWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);
    
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 32.0, vertical: 64.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 64,
              height: 64,
              decoration: BoxDecoration(
                color: theme.colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Icon(
                Icons.clinical_notes,
                size: 32,
                color: theme.colorScheme.onPrimaryContainer,
              ),
            ),
            const SizedBox(height: 40),
            Text(
              'Your skin,\nthoughtfully\nunderstood.',
              style: theme.textTheme.displayLarge,
            ),
            const Spacer(),
            Text(
              'An editorial approach to dermatological care. Professional, warm, and meticulously intentional.',
              style: theme.textTheme.bodyLarge?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: 48),
            ElevatedButton(
              onPressed: () {
                ref.read(navigationProvider.notifier).state = AppScreen.about;
              },
              child: const Text('BEGIN JOURNEY'),
            ),
          ],
        ),
      ),
    );
  }
}
