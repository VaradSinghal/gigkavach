import 'dart:ui';
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/payment_service.dart';

class PaymentProcessingOverlay extends StatefulWidget {
  final double amount;
  final String description;

  const PaymentProcessingOverlay({
    super.key,
    required this.amount,
    required this.description,
  });

  static void show(BuildContext context, {required double amount, required String description}) {
    showDialog(
      context: context,
      barrierColor: Colors.transparent,
      barrierDismissible: false,
      builder: (_) => PaymentProcessingOverlay(amount: amount, description: description),
    );
  }

  @override
  State<PaymentProcessingOverlay> createState() => _PaymentProcessingOverlayState();
}

class _PaymentProcessingOverlayState extends State<PaymentProcessingOverlay> with SingleTickerProviderStateMixin {
  final PaymentService _paymentService = PaymentService();
  PaymentStatus _status = PaymentStatus.initiating;
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _startProcess();
  }

  void _startProcess() {
    _paymentService.processPayout(
      amount: widget.amount,
      description: widget.description,
    ).listen((status) {
      if (mounted) {
        setState(() => _status = status);
        if (status == PaymentStatus.success) {
          _pulseController.stop();
        }
      }
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Stack(
        children: [
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(
                color: Colors.black.withValues(alpha: 0.6),
              ),
            ),
          ),
          Center(
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 32),
              padding: const EdgeInsets.all(32),
              decoration: BoxDecoration(
                color: AppColors.bgCard,
                borderRadius: BorderRadius.circular(28),
                border: Border.all(color: AppColors.textMuted.withValues(alpha: 0.2)),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.3),
                    blurRadius: 30,
                    spreadRadius: 5,
                  )
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  _buildIconArea(),
                  const SizedBox(height: 32),
                  _buildStatusText(),
                  const SizedBox(height: 16),
                  _buildDetails(),
                  const SizedBox(height: 32),
                  if (_status == PaymentStatus.success)
                    _buildCloseButton()
                  else
                    _buildStepIndicator(),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildIconArea() {
    if (_status == PaymentStatus.success) {
      return Container(
        height: 80,
        width: 80,
        decoration: const BoxDecoration(
          color: AppColors.success,
          shape: BoxShape.circle,
        ),
        child: const Icon(Icons.check_rounded, color: Colors.white, size: 48),
      );
    }

    return ScaleTransition(
      scale: Tween<double>(begin: 0.95, end: 1.05).animate(_pulseController),
      child: Container(
        height: 80,
        width: 80,
        decoration: BoxDecoration(
          color: AppColors.primary.withValues(alpha: 0.1),
          shape: BoxShape.circle,
        ),
        child: const Center(
          child: CircularProgressIndicator(
            color: AppColors.primary,
            strokeWidth: 3,
          ),
        ),
      ),
    );
  }

  Widget _buildStatusText() {
    String title = "";
    String sub = "";

    switch (_status) {
      case PaymentStatus.initiating:
        title = "Accessing Banking Gateway";
        sub = "Handshaking with payment architecture...";
      case PaymentStatus.authorizing:
        title = "Secure Authorization";
        sub = "Validating parametric trigger proof...";
      case PaymentStatus.transferring:
        title = "Dispatching Funds";
        sub = "Sending \u20B9${widget.amount.toInt()} via Generic Bank Transfer";
      case PaymentStatus.success:
        title = "Payment Successful";
        sub = "Funds have been added to your wallet.";
      case PaymentStatus.failed:
        title = "Transaction Pending";
        sub = "Network timeout. AI will retry shortly.";
    }

    return Column(
      children: [
        Text(
          title,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w800,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          sub,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 13,
            color: AppColors.textSecondary,
          ),
        ),
      ],
    );
  }

  Widget _buildDetails() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.bgDark,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text(
            "Generic Bank Payout",
            style: TextStyle(fontSize: 12, color: AppColors.textMuted),
          ),
          Text(
            "\u20B9${widget.amount.toInt()}",
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: AppColors.textPrimary,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStepIndicator() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(4, (index) {
        bool active = index <= _status.index;
        return Container(
          width: 24,
          height: 4,
          margin: const EdgeInsets.symmetric(horizontal: 4),
          decoration: BoxDecoration(
            color: active ? AppColors.primary : AppColors.textMuted.withValues(alpha: 0.2),
            borderRadius: BorderRadius.circular(2),
          ),
        );
      }),
    );
  }

  Widget _buildCloseButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: () => Navigator.pop(context),
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.success,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          elevation: 0,
        ),
        child: const Text("CONTINUE", style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1)),
      ),
    );
  }
}
