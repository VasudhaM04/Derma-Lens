import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/navigation_provider.dart';

class AboutScreen extends ConsumerWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => ref.read(navigationProvider.notifier).state = AppScreen.onboarding,
        ),
        title: const Text('About DermaLens'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: false,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            _buildInfoCard(context),
            const SizedBox(height: 24),
            _buildDisclaimerCard(context),
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: () => ref.read(navigationProvider.notifier).state = AppScreen.scan,
              child: const Text('CONTINUE TO SCAN'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: theme.colorScheme.secondary,
        borderRadius: BorderRadius.circular(32),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'What is DermaLens?',
            style: theme.textTheme.headlineMedium?.copyWith(color: Colors.white),
          ),
          const SizedBox(height: 12),
          const Text(
            'An AI-powered skin lesion classifier built for fairness and explainability across all skin tones.',
            style: TextStyle(color: Colors.white70, fontSize: 16, height: 1.5),
          ),
        ],
      ),
    );
  }

  Widget _buildDisclaimerCard(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceVariant,
        borderRadius: BorderRadius.circular(32),
        border: Border(
          left: BorderSide(color: theme.colorScheme.primaryContainer, width: 4),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.warning, color: theme.colorScheme.primary, size: 20),
              const SizedBox(width: 8),
              Text(
                'MEDICAL DISCLAIMER',
                style: theme.textTheme.labelMedium?.copyWith(
                  fontWeight: FontWeight.w800,
                  letterSpacing: 1.2,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          const Text(
            'DermaLens is a screening tool only. Results are not a substitute for professional medical diagnosis.',
            style: TextStyle(fontStyle: FontStyle.italic, color: Colors.black54),
          ),
        ],
      ),
    );
  }
}
