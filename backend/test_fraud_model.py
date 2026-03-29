"""
Test script to verify the Fraud Detection AI models are working properly.
"""
import os
import sys
from pprint import pprint
import random
import logging

logging.basicConfig(level=logging.ERROR)

sys.path.insert(0, os.path.dirname(__file__))
from insurance.services.claim_processor import ClaimProcessor
from fraud.services.validator import FraudValidator

def test_fraud_models():
    print("\n=" * 60)
    print("  GigKavach — Fraud Detection AI Verification Test")
    print("=" * 60)
    
    validator = FraudValidator()
    
    # CASE 1: 100% Legitimate Claim 
    # Proper environmental disruption, clean GPS, clean device, active worker
    print("\n[TEST CASE 1] CLEAN CLAIM (High Confidence)")
    clean_claim = {
        'rainfall_mm': 65,
        'aqi': 85,
        'temperature_c': 30,
        'inactive_hours': 6,
        'payout_amount': 420,
        'gps_consistent': True,
        'activity_coherent': True,
        'timing_correlated': True,
        'device_clean': True,
        'env_disruption': True
    }
    result_clean = validator.validate_claim(clean_claim)
    print(f"  Result Action: {result_clean['action_label']} | Score: {result_clean['confidence_score']}/100")
    if 'fraud_probability' in result_clean:
        print(f"  Fraud Probability: {result_clean['fraud_probability']:.2%}")
    
    # CASE 2: Suspicious Claim (Soft Review)
    # Environment was disrupted, but worker's GPS is inconsistent and timing is off
    print("\n[TEST CASE 2] SUSPICIOUS CLAIM (Medium Confidence / Soft Review)")
    suspicious_claim = {
        'rainfall_mm': 42,
        'aqi': 90,
        'temperature_c': 28,
        'inactive_hours': 4,
        'payout_amount': 280,
        'gps_consistent': False, # Inconsistent location
        'activity_coherent': True,
        'timing_correlated': False, # Timing doesn't match rain event
        'device_clean': True,
        'env_disruption': True
    }
    result_suspicious = validator.validate_claim(suspicious_claim)
    print(f"  Result Action: {result_suspicious['action_label']} | Score: {result_suspicious['confidence_score']}/100")
    if 'fraud_probability' in result_suspicious:
        print(f"  Fraud Probability: {result_suspicious['fraud_probability']:.2%}")

    # CASE 3: Syndicated / Fraudulent Claim (Rejection)
    # No actual weather disruption, device is spoofed, GPS is inconsistent
    print("\n[TEST CASE 3] FRAUDULENT CLAIM (Low Confidence / Rejection)")
    fraud_claim = {
        'rainfall_mm': 0,
        'aqi': 50,
        'temperature_c': 32,
        'inactive_hours': 8,
        'payout_amount': 600,
        'gps_consistent': False,
        'activity_coherent': False,
        'timing_correlated': False,
        'device_clean': False,     # VPN / Root detected
        'env_disruption': False    # No external APIs reported rain
    }
    result_fraud = validator.validate_claim(fraud_claim)
    print(f"  Result Action: {result_fraud['action_label']} | Score: {result_fraud['confidence_score']}/100")
    if 'fraud_probability' in result_fraud:
        print(f"  Fraud Probability: {result_fraud['fraud_probability']:.2%}")
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_fraud_models()
