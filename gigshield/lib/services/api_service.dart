import 'dart:convert';
import 'package:http/http.dart' as http;

/// GigKavach — Mobile API Bridge
/// Connects the Flutter application to the FastAPI AI Backend.
class GigKavachApiService {
  // Use the local IP of the machine running the backend (physical device requirement)
  static const String baseUrl = 'http://192.168.1.12:8000';

  /// Fetches a dynamic premium quote from the AI engine.
  static Future<Map<String, dynamic>> getPremiumQuote({
    required String workerId,
    required String zone,
    required String city,
    required String vehicleType,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/engine/evaluate'), // Or a specific premium endpoint if defined
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'worker_id': workerId,
          'zone': zone,
          'city': city,
          'vehicle_type': vehicleType,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to fetch premium from AI engine');
      }
    } catch (e) {
      print('API Error (Premium): $e');
      return {'error': e.toString(), 'fallback': true};
    }
  }

  /// Manually triggers a claim verification through the AI Fraud engine.
  static Future<Map<String, dynamic>> verifyAndSubmitClaim(Map<String, dynamic> claimData) async {
    try {
      // In a real flow, this might call /api/v1/claims/submit
      // For the demo, we use the simulation or engine evaluation triggers
      final response = await http.post(
        Uri.parse('$baseUrl/api/engine/evaluate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(claimData),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('AI Fraud Engine rejected or failed the request');
      }
    } catch (e) {
      print('API Error (Claim): $e');
      return {'status': 'pending', 'manual_review': true};
    }
  }

  /// Fetches dashboard summary for the worker.
  static Future<Map<String, dynamic>> getWorkerDashboard(String workerId) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/v1/dashboard/worker/$workerId'));
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      print('API Error (Dashboard): $e');
    }
    return {'protected_earnings': 0, 'active_coverage': false};
  }

  /// Polls the universal notification buffer for real-time mobile autonomous syncs.
  static Future<List<dynamic>> getNotifications() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/v1/notifications'));
      if (response.statusCode == 200) {
        return jsonDecode(response.body)['notifications'] ?? [];
      }
    } catch (e) {
      // Fail silently to avoid interrupting UX
    }
    return [];
  }
}
