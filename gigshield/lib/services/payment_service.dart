import 'dart:async';
import '../data/mock_data.dart';

enum PaymentStatus {
  initiating,
  authorizing,
  transferring,
  success,
  failed
}

class PaymentService {
  /// Simulates a generic bank payout/payment flow.
  /// Returns a stream of [PaymentStatus] updates to allow UI to react.
  Stream<PaymentStatus> processPayout({
    required double amount,
    required String description,
  }) async* {
    yield PaymentStatus.initiating;
    await Future.delayed(const Duration(milliseconds: 1500));

    yield PaymentStatus.authorizing;
    await Future.delayed(const Duration(milliseconds: 2000));

    yield PaymentStatus.transferring;
    await Future.delayed(const Duration(milliseconds: 2000));

    // Update Local Data
    _finalizeTransaction(amount, description);

    yield PaymentStatus.success;
  }

  void _finalizeTransaction(double amount, String description) {
    // Update balance
    MockData.walletBalance += amount;
    MockData.totalPayoutsReceived += amount;
    MockData.totalClaimsPaid += 1;

    // Add to transaction history
    MockData.walletTransactions.insert(0, {
      'type': 'credit',
      'amount': amount,
      'desc': description,
      'date': 'Just Now',
      'status': 'Completed',
    });
  }
}
