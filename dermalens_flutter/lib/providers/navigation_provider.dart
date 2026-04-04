import 'package:flutter_riverpod/flutter_riverpod.dart';

enum AppScreen {
  onboarding,
  about,
  scan,
  results,
}

final navigationProvider = StateProvider<AppScreen>((ref) => AppScreen.onboarding);
