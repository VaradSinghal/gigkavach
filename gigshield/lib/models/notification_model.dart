import 'package:flutter/material.dart';

enum NotificationType { payout, risk, info, alert }

class GigKavachNotification {
  final String id;
  final String title;
  final String message;
  final NotificationType type;
  final DateTime timestamp;
  bool isRead;

  GigKavachNotification({
    required this.id,
    required this.title,
    required this.message,
    required this.type,
    required this.timestamp,
    this.isRead = false,
  });

  IconData get icon {
    switch (type) {
      case NotificationType.payout:
        return Icons.account_balance_wallet_rounded;
      case NotificationType.risk:
        return Icons.warning_rounded;
      case NotificationType.alert:
        return Icons.notifications_active_rounded;
      case NotificationType.info:
      default:
        return Icons.info_outline_rounded;
    }
  }

  Color get color {
    switch (type) {
      case NotificationType.payout:
        return const Color(0xFF098551); // success
      case NotificationType.risk:
        return const Color(0xFFE94B4B); // danger
      case NotificationType.alert:
        return const Color(0xFFF7A23B); // warning
      case NotificationType.info:
      default:
        return const Color(0xFF0052FF); // primary
    }
  }
}
