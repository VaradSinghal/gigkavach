import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../data/mock_data.dart';
import '../widgets/common_widgets.dart';

class BoostScreen extends StatelessWidget {
  const BoostScreen({super.key});

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
                'Earnings Boost',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w700,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 4),
              const Text(
                'AI-powered zone recommendations to maximize your earnings',
                style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
              ),
              const SizedBox(height: 20),
              _buildDecisionCard(),
              const SectionHeader(title: 'Hot Zones Right Now'),
              _buildZoneList(),
              const SectionHeader(title: 'Segment Demand'),
              _buildSegmentDemand(),
              const SectionHeader(title: 'Weekly Forecast'),
              _buildWeekForecast(),
              const SizedBox(height: 100),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDecisionCard() {
    return GlassCard(
      child: Column(
        children: [
          Row(
            children: [
              _scoreRing(),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Work Decision Score',
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.textSecondary,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      MockData.decisionLabel,
                      style: const TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.w800,
                        color: AppColors.success,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          _scoreBreakdownBar('Demand', MockData.demandScore, AppColors.accent),
          const SizedBox(height: 8),
          _scoreBreakdownBar(
            'Weather Safety',
            MockData.weatherSafety,
            AppColors.success,
          ),
          const SizedBox(height: 8),
          _scoreBreakdownBar(
            'Coverage Bonus',
            MockData.coverageBonus,
            AppColors.primary,
          ),
          const SizedBox(height: 8),
          _scoreBreakdownBar(
            'Historical',
            MockData.historicalStability,
            AppColors.warning,
          ),
        ],
      ),
    );
  }

  Widget _scoreRing() {
    final score = MockData.decisionScore;
    final color = score >= 65
        ? AppColors.success
        : score >= 35
        ? AppColors.warning
        : AppColors.danger;

    return SizedBox(
      width: 70,
      height: 70,
      child: Stack(
        alignment: Alignment.center,
        children: [
          SizedBox(
            width: 70,
            height: 70,
            child: CircularProgressIndicator(
              value: score / 100,
              strokeWidth: 6,
              backgroundColor: AppColors.bgSurface,
              valueColor: AlwaysStoppedAnimation<Color>(color),
              strokeCap: StrokeCap.round,
            ),
          ),
          Text(
            '$score',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.w800,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Widget _scoreBreakdownBar(String label, double value, Color color) {
    return Row(
      children: [
        SizedBox(
          width: 100,
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 12,
              color: AppColors.textSecondary,
            ),
          ),
        ),
        Expanded(
          child: ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: value / 100,
              minHeight: 6,
              backgroundColor: AppColors.bgSurface,
              valueColor: AlwaysStoppedAnimation<Color>(color),
            ),
          ),
        ),
        const SizedBox(width: 8),
        SizedBox(
          width: 30,
          child: Text(
            '${value.toInt()}',
            textAlign: TextAlign.right,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: color,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildZoneList() {
    return Column(
      children: MockData.boostZones.map((zone) {
        final score = zone['score'] as int;
        final color = score >= 85
            ? AppColors.success
            : score >= 70
            ? AppColors.accent
            : AppColors.warning;

        return Padding(
          padding: const EdgeInsets.only(bottom: 10),
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
                      '$score',
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
                        'Peak: ${zone['peakTime']} - ${zone['distance']}',
                        style: const TextStyle(
                          fontSize: 11,
                          color: AppColors.textSecondary,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.success.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    zone['estimatedBoost'] as String,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                      color: AppColors.success,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildSegmentDemand() {
    final segments = [
      {
        'name': 'Food Delivery',
        'demand': 0.75,
        'color': AppColors.primary,
        'label': 'High',
      },
      {
        'name': 'Grocery',
        'demand': 0.92,
        'color': AppColors.success,
        'label': 'Very High',
      },
      {
        'name': 'Hyperlocal',
        'demand': 0.45,
        'color': AppColors.warning,
        'label': 'Medium',
      },
    ];

    return GlassCard(
      child: Column(
        children: segments.map((seg) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      seg['name'] as String,
                      style: const TextStyle(
                        fontSize: 13,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    StatusChip(
                      label: seg['label'] as String,
                      color: seg['color'] as Color,
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: seg['demand'] as double,
                    minHeight: 8,
                    backgroundColor: AppColors.bgSurface,
                    valueColor: AlwaysStoppedAnimation<Color>(
                      seg['color'] as Color,
                    ),
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildWeekForecast() {
    return GlassCard(
      child: Column(
        children: MockData.weekForecast.map((day) {
          final risk = day['risk'] as int;
          final color = risk >= 60
              ? AppColors.danger
              : risk >= 40
              ? AppColors.warning
              : AppColors.success;

          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Row(
              children: [
                SizedBox(
                  width: 36,
                  child: Text(
                    day['day'] as String,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w500,
                      color: AppColors.textPrimary,
                    ),
                  ),
                ),
                Expanded(
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: risk / 100,
                      minHeight: 8,
                      backgroundColor: AppColors.bgSurface,
                      valueColor: AlwaysStoppedAnimation<Color>(color),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                SizedBox(
                  width: 40,
                  child: Text(
                    day['rain'] as String,
                    textAlign: TextAlign.right,
                    style: const TextStyle(
                      fontSize: 11,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                SizedBox(
                  width: 50,
                  child: StatusChip(
                    label: day['demand'] as String,
                    color: (day['demand'] as String) == 'High'
                        ? AppColors.success
                        : (day['demand'] as String) == 'Medium'
                        ? AppColors.warning
                        : AppColors.danger,
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }
}
