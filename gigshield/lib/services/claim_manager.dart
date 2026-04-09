import 'dart:math';
import 'package:flutter/foundation.dart';
import 'supabase_service.dart';
import 'api_service.dart';

// ... (ClaimEvent and other code unchanged)

class ClaimManager extends ChangeNotifier {
  // ... (singleton and list unchanged)

  /// Evaluates and submits a new parametric claim
  /// Now connects to the FastAPI AI Backend for real-time Fraud verification.
  Future<ClaimEvent?> submitParametricClaim({
    required String workerId,
    required String triggerId,
    required String triggerLabel,
    required String triggerData,
    required Map<String, dynamic> zoneInfo,
    required double baseHourlyRate,
    required double coverageMultiplier,
  }) async {
    // 1. Local Pre-validation (Duplicates)
    final today = DateTime.now().toIso8601String().split('T')[0];
    final existingToday = _claims.where((c) => 
      c.triggerId == triggerId && 
      c.timestamp.toIso8601String().startsWith(today)
    ).toList();

    if (existingToday.isNotEmpty) {
      debugPrint('Claim already exists for $triggerId today. Skipping.');
      return null;
    }

    // 2. Prepare Payload for AI Backend
    final payload = {
      'worker_id': workerId,
      'trigger_type': triggerId,
      'trigger_label': triggerLabel,
      'trigger_data': triggerData,
      'zone': zoneInfo['zone'] ?? 'Unknown',
      'city': zoneInfo['city'] ?? 'Unknown',
      'base_rate': baseHourlyRate,
      'multiplier': coverageMultiplier,
      'timestamp': DateTime.now().toIso8601String(),
    };

    // 3. Trigger Real-time AI Verification (Fraud Engine)
    final aiResult = await GigKavachApiService.verifyAndSubmitClaim(payload);
    
    // 4. Map API Result to Claim Event
    final claimId = aiResult['claim_id'] ?? 'CLM-${DateTime.now().millisecondsSinceEpoch.toString().substring(5)}';
    final status = aiResult['status'] ?? ( (aiResult['confidence'] ?? 0) > 85 ? 'approved' : 'validating' );
    final payoutAmount = (aiResult['payout_amount'] as num?)?.toDouble() ?? (5 * baseHourlyRate * coverageMultiplier);

    final newClaim = ClaimEvent(
      claimId: claimId,
      triggerId: triggerId,
      label: triggerLabel,
      timestamp: DateTime.now(),
      status: status,
      payoutAmount: payoutAmount,
      isSustained: aiResult['is_sustained'] ?? false,
    );

    _claims.insert(0, newClaim);
    notifyListeners();

    debugPrint('AI Backend Claim Processed: $claimId (Status: $status)');
    return newClaim;
  }
}
}
