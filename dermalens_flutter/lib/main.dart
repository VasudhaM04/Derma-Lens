import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'theme/app_theme.dart';
import 'screens/onboarding_screen.dart';
import 'screens/about_screen.dart';
import 'screens/scan_screen.dart';
import 'screens/results_screen.dart';
import 'providers/navigation_provider.dart';

void main() {
  runApp(
    const ProviderScope(
      child: DermaLensApp(),
    ),
  );
}

class DermaLensApp extends ConsumerWidget {
  const DermaLensApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final screen = ref.watch(navigationProvider);

    return MaterialApp(
      title: 'DermaLens',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: _getScreen(screen),
    );
  }

  Widget _getScreen(AppScreen screen) {
    switch (screen) {
      case AppScreen.onboarding:
        return const OnboardingScreen();
      case AppScreen.about:
        return const AboutScreen();
      case AppScreen.scan:
        return const ScanScreen();
      case AppScreen.results:
        return const ResultsScreen();
    }
  }
}
