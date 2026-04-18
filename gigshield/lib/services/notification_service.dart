import 'package:flutter/material.dart';
import '../models/notification_model.dart';

class NotificationService extends ChangeNotifier {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  final List<GigKavachNotification> _notifications = [];
  
  List<GigKavachNotification> get notifications => List.unmodifiable(_notifications.reversed);
  
  int get unreadCount => _notifications.where((n) => !n.isRead).length;

  void addNotification({
    required String id,
    required String title,
    required String message,
    required NotificationType type,
  }) {
    // Avoid duplicates if same ID is polled multiple times
    if (_notifications.any((n) => n.id == id)) return;

    _notifications.add(GigKavachNotification(
      id: id,
      title: title,
      message: message,
      type: type,
      timestamp: DateTime.now(),
    ));
    
    notifyListeners();
  }

  void markAsRead(String id) {
    final index = _notifications.indexWhere((n) => n.id == id);
    if (index != -1 && !_notifications[index].isRead) {
      _notifications[index].isRead = true;
      notifyListeners();
    }
  }

  void markAllAsRead() {
    for (var n in _notifications) {
      n.isRead = true;
    }
    notifyListeners();
  }

  void clearAll() {
    _notifications.clear();
    notifyListeners();
  }
}
