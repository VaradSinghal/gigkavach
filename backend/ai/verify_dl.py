import os
import sys

# Add project root to path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(ROOT_DIR, 'backend', 'ai'))

from model_loader import loader

def test_loader():
    print("Testing GigKavach Model Loader with Torch assets...")
    loader.load_all()
    
    # Test Premium Inference
    premium_input = {
        'avg_daily_income': 700,
        'claim_rate': 0.05,
        'trust_score': 0.9,
        'avg_rainfall_mm': 10,
        'experience_weeks': 20
    }
    res = loader.predict_premium(premium_input)
    print(f"\nPremium Prediction: {res['premium']}")
    
    # Test Fraud Inference
    fraud_input = {
        'integrity_score': 95,
        'gps_consistent': 1,
        'activity_coherent': 1,
        'timing_correlated': 1,
        'device_clean': 1,
        'env_disruption': 5
    }
    f_res = loader.predict_fraud_score(fraud_input)
    print(f"Fraud Confidence: {f_res['confidence']}% (Action: {f_res['action']})")
    
    if isinstance(loader.premium_model, torch.nn.Module):
        print("\n[SUCCESS] Loader is successfully using PyTorch backends.")
    else:
        print("\n[WARNING] Loader is still using Scikit-Learn backends.")

if __name__ == '__main__':
    import torch
    test_loader()
