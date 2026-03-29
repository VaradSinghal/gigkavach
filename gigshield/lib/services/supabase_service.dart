import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class SupabaseService {
  static SupabaseClient get client => Supabase.instance.client;

  static Future<void> initialize() async {
    await dotenv.load(fileName: ".env");

    final supabaseUrl = dotenv.env['SUPABASE_URL'] ?? '';
    final supabaseAnonKey = dotenv.env['SUPABASE_ANON_KEY'] ?? '';

    if (supabaseUrl.isEmpty ||
        supabaseAnonKey.isEmpty ||
        supabaseUrl == 'YOUR_SUPABASE_PROJECT_URL') {
      print('⚠ SUPABASE_URL or SUPABASE_ANON_KEY missing/invalid in .env');
      print('  Running Flutter app in LOCAL MOCK mode (No remote sync).');
      return;
    }

    try {
      await Supabase.initialize(url: supabaseUrl, anonKey: supabaseAnonKey);
      print('✓ Connected to Supabase backend.');
    } catch (e) {
      print('⚠ Failed to connect to Supabase: $e');
    }
  }

  static bool get isConfigured {
    try {
      return Supabase.instance.client != null;
    } catch (e) {
      return false;
    }
  }
}
