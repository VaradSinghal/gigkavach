"""
GigKavach — Master Training Script
Runs all model training pipelines in sequence.
Usage: python train_all.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from training.train_premium_model import train as train_premium
from training.train_zone_risk_model import train as train_zone_risk
from training.train_fraud_model import train as train_fraud
from training.train_boost_model import train as train_boost
from training.train_forecast_model import train as train_forecast


def train_all():
    print("\n" + "=" * 60)
    print("  GigKavach -- Full ML Pipeline Training")
    print("  Training 5 models for gig worker protection")
    print("=" * 60)

    start = time.time()
    results = {}

    # 1. Premium Pricing
    print("\n\n" + "-" * 60)
    print("  [1/5] PREMIUM PRICING MODEL")
    print("-" * 60)
    try:
        train_premium()
        results['premium'] = '[DONE]'
    except Exception as e:
        results['premium'] = f'[FAILED] {e}'
        print(f"  ERROR: {e}")

    # 2. Zone Risk Clustering
    print("\n\n" + "-" * 60)
    print("  [2/5] ZONE RISK CLUSTERING MODEL")
    print("-" * 60)
    try:
        train_zone_risk()
        results['zone_risk'] = '[DONE]'
    except Exception as e:
        results['zone_risk'] = f'[FAILED] {e}'
        print(f"  ERROR: {e}")

    # 3. Fraud Detection
    print("\n\n" + "-" * 60)
    print("  [3/5] FRAUD DETECTION MODEL")
    print("-" * 60)
    try:
        train_fraud()
        results['fraud'] = '[DONE]'
    except Exception as e:
        results['fraud'] = f'[FAILED] {e}'
        print(f"  ERROR: {e}")

    # 4. Earnings Boost
    print("\n\n" + "-" * 60)
    print("  [4/5] EARNINGS BOOST MODEL")
    print("-" * 60)
    try:
        train_boost()
        results['boost'] = '[DONE]'
    except Exception as e:
        results['boost'] = f'[FAILED] {e}'
        print(f"  ERROR: {e}")

    # 5. Risk Forecast
    print("\n\n" + "-" * 60)
    print("  [5/5] RISK FORECAST MODEL")
    print("-" * 60)
    try:
        train_forecast()
        results['forecast'] = '[DONE]'
    except Exception as e:
        results['forecast'] = f'[FAILED] {e}'
        print(f"  ERROR: {e}")

    elapsed = time.time() - start

    print("\n\n" + "=" * 60)
    print("  TRAINING SUMMARY")
    print("=" * 60)
    for model, status in results.items():
        print(f"  {model:20s} {status}")
    print(f"\n  Total time: {elapsed:.1f}s")
    print("=" * 60)


if __name__ == '__main__':
    train_all()
