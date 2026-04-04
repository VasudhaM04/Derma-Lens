import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const Color primary = Color(0xFF5A6241);
  static const Color primaryContainer = Color(0xFFA7B08A);
  static const Color onPrimaryContainer = Color(0xFF3B4325);
  
  static const Color surface = Color(0xFFFCF9F2);
  static const Color surfaceContainer = Color(0xFFF1EEE7);
  static const Color onSurface = Color(0xFF1C1C18);
  static const Color onSurfaceVariant = Color(0xFF46483E);
  static const Color secondary = Color(0xFF6F5A51);

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primary,
        primary: primary,
        onPrimary: Colors.white,
        primaryContainer: primaryContainer,
        onPrimaryContainer: onPrimaryContainer,
        surface: surface,
        onSurface: onSurface,
        secondary: secondary,
      ),
      scaffoldBackgroundColor: surface,
      textTheme: GoogleFonts.plusJakartaSansTextTheme().copyWith(
        displayLarge: GoogleFonts.plusJakartaSans(
          fontSize: 56,
          fontWeight: FontWeight.w300,
          color: primary,
          letterSpacing: -1.5,
        ),
        headlineMedium: GoogleFonts.plusJakartaSans(
          fontSize: 24,
          fontWeight: FontWeight.w700,
          color: onSurface,
        ),
        bodyLarge: GoogleFonts.plusJakartaSans(
          fontSize: 16,
          height: 1.6,
          color: onSurface,
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryContainer,
          foregroundColor: onPrimaryContainer,
          minimumSize: const Size(double.infinity, 56),
          shape: const StadiumBorder(),
          elevation: 0,
          textStyle: GoogleFonts.plusJakartaSans(
            fontWeight: FontWeight.w700,
            letterSpacing: 1.2,
          ),
        ),
      ),
    );
  }
}
