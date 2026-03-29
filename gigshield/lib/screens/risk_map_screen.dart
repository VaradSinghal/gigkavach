import 'dart:math';
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/mock_data.dart';
import '../widgets/common_widgets.dart';

class RiskMapScreen extends StatelessWidget {
  const RiskMapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.bgDark,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),
              const Text(
                'Risk Map',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w700,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 4),
              const Text(
                'Real-time disruption risk across Chennai zones',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
              const SizedBox(height: 20),
              _buildMapPlaceholder(),
              const SizedBox(height: 8),
              _buildLegend(),
              const SectionHeader(title: 'Zone Risk Scores'),
              _buildZoneList(),
              const SizedBox(height: 100),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMapPlaceholder() {
    return Container(
      height: 220,
      decoration: BoxDecoration(
        color: AppColors.bgCard,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.textMuted.withValues(alpha: 0.3)),
      ),
      child: Stack(
        children: [
          // Grid pattern to simulate map
          ClipRRect(
            borderRadius: BorderRadius.circular(16),
            child: CustomPaint(
              size: const Size(double.infinity, 220),
              painter: _HexGridPainter(),
            ),
          ),
          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.bgDark.withValues(alpha: 0.8),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(
                    Icons.map_rounded,
                    color: AppColors.primary,
                    size: 28,
                  ),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.bgDark.withValues(alpha: 0.8),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: const Text(
                    'Mapbox Integration Zone',
                    style: TextStyle(
                      fontSize: 12,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLegend() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _legendItem(AppColors.success, 'Low'),
        const SizedBox(width: 16),
        _legendItem(AppColors.warning, 'Moderate'),
        const SizedBox(width: 16),
        _legendItem(AppColors.danger, 'High'),
        const SizedBox(width: 16),
        _legendItem(const Color(0xFFE84393), 'Critical'),
      ],
    );
  }

  Widget _legendItem(Color color, String label) {
    return Row(
      children: [
        Container(
          width: 10,
          height: 10,
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(3),
          ),
        ),
        const SizedBox(width: 4),
        Text(
          label,
          style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
        ),
      ],
    );
  }

  Widget _buildZoneList() {
    final sortedZones = List<Map<String, dynamic>>.from(MockData.riskZones)
      ..sort((a, b) => (b['risk'] as int).compareTo(a['risk'] as int));

    return Column(
      children: sortedZones.map((zone) {
        final risk = zone['risk'] as int;
        Color color;
        if (risk >= 80) {
          color = const Color(0xFFE84393);
        } else if (risk >= 60) {
          color = AppColors.danger;
        } else if (risk >= 40) {
          color = AppColors.warning;
        } else {
          color = AppColors.success;
        }

        return Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: GlassCard(
            padding: const EdgeInsets.all(14),
            child: Row(
              children: [
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    color: color.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Center(
                    child: Text(
                      '$risk',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w800,
                        color: color,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        zone['zone'] as String,
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        'Rainfall: ${zone['rain']}',
                        style: const TextStyle(
                          fontSize: 11,
                          color: AppColors.textSecondary,
                        ),
                      ),
                    ],
                  ),
                ),
                StatusChip(label: zone['label'] as String, color: color),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}

class _HexGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.textMuted.withValues(alpha: 0.1)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 0.5;

    const hexSize = 30.0;
    final rows = (size.height / (hexSize * 1.5)).ceil() + 1;
    final cols = (size.width / (hexSize * 1.73)).ceil() + 1;

    for (var row = 0; row < rows; row++) {
      for (var col = 0; col < cols; col++) {
        final offset = row.isOdd ? hexSize * 0.87 : 0.0;
        final cx = col * hexSize * 1.73 + offset;
        final cy = row * hexSize * 1.5;
        _drawHex(canvas, Offset(cx, cy), hexSize, paint);
      }
    }

    // Draw some colored hexes to represent risk zones
    final riskPaint = Paint()..style = PaintingStyle.fill;
    final riskAreas = [
      (
        Offset(size.width * 0.3, size.height * 0.4),
        AppColors.danger.withValues(alpha: 0.2),
      ),
      (
        Offset(size.width * 0.7, size.height * 0.3),
        AppColors.success.withValues(alpha: 0.2),
      ),
      (
        Offset(size.width * 0.5, size.height * 0.6),
        AppColors.warning.withValues(alpha: 0.2),
      ),
      (
        Offset(size.width * 0.2, size.height * 0.7),
        const Color(0xFFE84393).withValues(alpha: 0.2),
      ),
      (
        Offset(size.width * 0.8, size.height * 0.7),
        AppColors.success.withValues(alpha: 0.2),
      ),
    ];

    for (final area in riskAreas) {
      riskPaint.color = area.$2;
      _drawHex(canvas, area.$1, hexSize * 1.5, riskPaint);
    }
  }

  void _drawHex(Canvas canvas, Offset center, double size, Paint paint) {
    final path = Path();
    for (var i = 0; i < 6; i++) {
      final angle = (60 * i - 30) * pi / 180;
      final x = center.dx + size * 0.5 * cos(angle) * 1.73;
      final y = center.dy + size * 0.5 * sin(angle) * 1.73;
      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    path.close();
    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
