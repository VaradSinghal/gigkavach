import 'package:flutter/material.dart';
import 'dart:ui';
import '../theme/app_theme.dart';
import '../services/claim_manager.dart';

import '../widgets/payment_processing_overlay.dart';

class DemoClaimOverlay extends StatefulWidget {
  final Map<String, dynamic> mockParams;

  const DemoClaimOverlay({super.key, required this.mockParams});

  static void show(BuildContext context) {
    showDialog(
      context: context,
      barrierColor: Colors.transparent,
      barrierDismissible: false,
      builder: (_) => DemoClaimOverlay(
        mockParams: const {
          'type': 'flash_flood',
          'label': 'Flash Flood Alert (Simulated)',
          'data': '125mm Rainfall / IMD Red Alert',
        },
      ),
    );
  }

  @override
  State<DemoClaimOverlay> createState() => _DemoClaimOverlayState();
}

class _DemoClaimOverlayState extends State<DemoClaimOverlay> with TickerProviderStateMixin {
  int _currentStep = 0;
  ClaimEvent? _finalClaim;
  bool _finished = false;

  final List<String> _steps = [
    "Intercepting Civic Warning Matrix...",
    "Validating GPS & Sensor Parity...",
    "Mapping Policy against Historical Models...",
    "Executing Zero-Touch Auto-Approval...",
  ];

  late AnimationController _fadeController;
  late Animation<double> _fadeAnim;

  @override
  void initState() {
    super.initState();
    _fadeController = AnimationController(vsync: this, duration: const Duration(milliseconds: 600));
    _fadeAnim = Tween<double>(begin: 0, end: 1).animate(CurvedAnimation(parent: _fadeController, curve: Curves.easeOut));
    _fadeController.forward();

    _runDemoSequence();
  }

  Future<void> _runDemoSequence() async {
    for (int i = 0; i < _steps.length; i++) {
      await Future.delayed(const Duration(milliseconds: 1200));
      if (mounted) setState(() => _currentStep = i);
    }

    // Actually run the claim processor
    final claim = await ClaimManager().submitParametricClaim(
      workerId: 'DEMO_USER_99',
      triggerId: widget.mockParams['type'],
      triggerLabel: widget.mockParams['label'],
      triggerData: widget.mockParams['data'],
      zoneInfo: {'zone': 'Adyar (Simulated)', 'city': 'Chennai'},
      baseHourlyRate: 70.0,
      coverageMultiplier: 0.70,
    );

    await Future.delayed(const Duration(milliseconds: 600));
    if (mounted) {
      setState(() {
        _finalClaim = claim;
        _finished = true;
      });
    }
  }

  @override
  void dispose() {
    _fadeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: Stack(
        children: [
          // Glass blur backdrop
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
              child: Container(
                color: AppColors.onboardBg.withValues(alpha: 0.8),
              ),
            ),
          ),
          Center(
            child: FadeTransition(
              opacity: _fadeAnim,
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 24),
                padding: const EdgeInsets.all(32),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.onboardBluePrimary.withValues(alpha: 0.15),
                      blurRadius: 40,
                      spreadRadius: 10,
                    )
                  ],
                  border: Border.all(color: AppColors.onboardBorder),
                ),
                child: _finished ? _buildSuccessState() : _buildProgressState(),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProgressState() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const SizedBox(
          width: 60,
          height: 60,
          child: CircularProgressIndicator(
            color: AppColors.onboardBluePrimary,
            backgroundColor: AppColors.onboardBlueSoft,
            strokeWidth: 4,
          ),
        ),
        const SizedBox(height: 32),
        Text(
          'Live AI Processing',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w800,
            color: AppColors.onboardTextDark,
          ),
        ),
        const SizedBox(height: 24),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: List.generate(_steps.length, (index) {
            bool isActive = _currentStep == index;
            bool isDone = _currentStep > index;

            return Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: Row(
                children: [
                  Icon(
                    isDone ? Icons.check_circle_rounded : (isActive ? Icons.sync : Icons.radio_button_unchecked),
                    color: isDone ? AppColors.success : (isActive ? AppColors.onboardBluePrimary : AppColors.onboardTextMuted),
                    size: 20,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      _steps[index],
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: isActive || isDone ? FontWeight.w600 : FontWeight.w400,
                        color: isDone || isActive ? AppColors.onboardTextDark : AppColors.onboardTextMuted,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }),
        ),
      ],
    );
  }

  Widget _buildSuccessState() {
    bool isDuplicate = _finalClaim == null;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: isDuplicate ? AppColors.warning.withValues(alpha: 0.1) : AppColors.success.withValues(alpha: 0.1),
          ),
          child: Icon(
            isDuplicate ? Icons.warning_rounded : Icons.check_circle_rounded,
            color: isDuplicate ? AppColors.warning : AppColors.success,
            size: 64,
          ),
        ),
        const SizedBox(height: 24),
        Text(
          isDuplicate ? 'Duplicate Event Blocked' : 'Zero-Touch Claim Approved',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w800,
            color: AppColors.onboardTextDark,
          ),
        ),
        const SizedBox(height: 12),
        Text(
          isDuplicate 
            ? 'Our ML detected identical signals today. Fraud bypass successful.'
            : 'Funds have been dispatched instantly to your local wallet architecture based on parametric triggers.',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 14,
            color: AppColors.onboardTextBody,
          ),
        ),
        if (!isDuplicate) ...[
          const SizedBox(height: 24),
          Container(
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
            decoration: BoxDecoration(
              color: AppColors.onboardBlueSoft,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Auto-Payout',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.onboardBluePrimary,
                  ),
                ),
                Text(
                  '₹${_finalClaim!.payoutAmount.toInt()}',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.w800,
                    color: AppColors.onboardTextDark,
                  ),
                ),
              ],
            ),
          ),
        ],
        const SizedBox(height: 32),
        SizedBox(
          width: double.infinity,
          height: 50,
          child: ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              if (_finalClaim != null) {
                PaymentProcessingOverlay.show(
                  context,
                  amount: _finalClaim!.payoutAmount,
                  description: 'Manual Simulation: ${_finalClaim!.label}',
                );
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.onboardBluePrimary,
              elevation: 0,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            child: Text(
              _finalClaim != null ? 'PROCESS Payout' : 'Back to Dashboard', 
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: Colors.white)
            ),
          ),
        ),
      ],
    );
  }
}
