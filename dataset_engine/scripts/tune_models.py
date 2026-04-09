import os
import torch
import torch.nn as nn
import torch.optim as optim
import optuna
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from dl_models import create_model

# Load features from backend feature_engineering if possible, 
# but for standalone dataset_engine we'll use a direct path or copy logic
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(ROOT_DIR, 'backend', 'ai'))
from pipelines.feature_engineering import engineer_premium_features, engineer_fraud_features

DATA_DIR = os.path.join(ROOT_DIR, 'dataset_engine', 'data')
MODEL_SAVE_DIR = os.path.join(ROOT_DIR, 'dataset_engine', 'models')
os.makedirs(MODEL_SAVE_DIR, exist_ok=True)

def get_premium_data():
    workers_df = pd.read_csv(os.path.join(DATA_DIR, 'workers.csv'))
    weather_df = pd.read_csv(os.path.join(DATA_DIR, 'weather.csv'))
    zones_df = pd.read_csv(os.path.join(DATA_DIR, 'zones.csv'))
    claims_df = pd.read_csv(os.path.join(DATA_DIR, 'claims.csv'))
    
    features_df = engineer_premium_features(workers_df, weather_df, claims_df, zones_df)
    
    FEATURE_COLS = [
        'avg_daily_income', 'avg_weekly_income', 'avg_daily_hours',
        'experience_weeks', 'is_flood_zone', 'trust_score',
        'elevation_m', 'drainage_score', 'historical_flood_events',
        'historical_disruption_days', 'road_density',
        'avg_rainfall_mm', 'max_rainfall_mm', 'avg_aqi', 'heavy_rain_day_ratio',
        'claim_count', 'claim_rate', 'total_payout',
    ]
    
    X = features_df[FEATURE_COLS].values
    y = features_df['target_premium'].values.reshape(-1, 1)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    
    return torch.FloatTensor(X_train), torch.FloatTensor(X_val), torch.FloatTensor(y_train), torch.FloatTensor(y_val), len(FEATURE_COLS)

def get_fraud_data():
    claims_df = pd.read_csv(os.path.join(DATA_DIR, 'claims.csv'))
    features_df = engineer_fraud_features(claims_df)
    
    FRAUD_FEATURES = [
        'rainfall_mm', 'aqi', 'temperature_c',
        'inactive_hours', 'payout_amount',
        'gps_consistent', 'activity_coherent',
        'timing_correlated', 'device_clean',
        'env_disruption', 'integrity_score',
    ]
    
    X = features_df[FRAUD_FEATURES].values
    y = features_df['is_fraud'].values.reshape(-1, 1).astype(float)
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    
    return torch.FloatTensor(X_train), torch.FloatTensor(X_val), torch.FloatTensor(y_train), torch.FloatTensor(y_val), len(FRAUD_FEATURES)

def premium_objective(trial):
    X_train, X_val, y_train, y_val, input_dim = get_premium_data()
    
    n_layers = trial.suggest_int('n_layers', 1, 3)
    hidden_layers = [trial.suggest_int(f'n_units_l{i}', 16, 128) for i in range(n_layers)]
    lr = trial.suggest_float('lr', 1e-5, 1e-2, log=True)
    dropout = trial.suggest_float('dropout', 0.1, 0.5)
    
    model = create_model(input_dim, hidden_layers, 1, dropout, 'regression')
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    # Simple training loop
    model.train()
    for epoch in range(50): # Reduced epochs for HPO speed
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        
    model.eval()
    with torch.no_grad():
        val_output = model(X_val)
        val_loss = criterion(val_output, y_val).item()
        
    return val_loss

def fraud_objective(trial):
    X_train, X_val, y_train, y_val, input_dim = get_fraud_data()
    
    n_layers = trial.suggest_int('n_layers', 1, 3)
    hidden_layers = [trial.suggest_int(f'n_units_l{i}', 16, 128) for i in range(n_layers)]
    lr = trial.suggest_float('lr', 1e-4, 1e-2, log=True)
    dropout = trial.suggest_float('dropout', 0.1, 0.4)
    
    model = create_model(input_dim, hidden_layers, 1, dropout, 'classification')
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()
    
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        loss = criterion(model(X_train), y_train)
        loss.backward()
        optimizer.step()
        
    model.eval()
    with torch.no_grad():
        val_loss = criterion(model(X_val), y_val).item()
        
    return val_loss

def run_tuning():
    print("Tuning Premium Pricing Model...")
    study = optuna.create_study(direction='minimize')
    study.optimize(premium_objective, n_trials=20)
    
    print("Best Trial:", study.best_params)
    
    # Save best parameters to a file or just use them to train a final 'Base' model
    # For now, let's train a final one with best params and save it
    X_train, X_val, y_train, y_val, input_dim = get_premium_data()
    best = study.best_params
    hidden_layers = [best[f'n_units_l{i}'] for i in range(best['n_layers'])]
    
    final_model = create_model(input_dim, hidden_layers, 1, best['dropout'], 'regression')
    optimizer = optim.Adam(final_model.parameters(), lr=best['lr'])
    criterion = nn.MSELoss()
    
    for epoch in range(200):
        final_model.train()
        optimizer.zero_grad()
        loss = criterion(final_model(X_train), y_train)
        loss.backward()
        optimizer.step()
        
    final_model.save(os.path.join(MODEL_SAVE_DIR, 'premium_base.pt'))
    print(f"[DONE] Saved Best Premium Model to {MODEL_SAVE_DIR}")

    print("\n" + "="*40)
    print("Tuning Fraud Detection Model...")
    fraud_study = optuna.create_study(direction='minimize')
    fraud_study.optimize(fraud_objective, n_trials=20)
    
    print("Best Fraud Params:", fraud_study.best_params)
    
    X_train, X_val, y_train, y_val, input_dim = get_fraud_data()
    f_best = fraud_study.best_params
    f_hidden = [f_best[f'n_units_l{i}'] for i in range(f_best['n_layers'])]
    
    final_fraud = create_model(input_dim, f_hidden, 1, f_best['dropout'], 'classification')
    f_optimizer = optim.Adam(final_fraud.parameters(), lr=f_best['lr'])
    f_criterion = nn.BCELoss()
    
    for epoch in range(150):
        final_fraud.train()
        f_optimizer.zero_grad()
        f_loss = f_criterion(final_fraud(X_train), y_train)
        f_loss.backward()
        f_optimizer.step()
        
    final_fraud.save(os.path.join(MODEL_SAVE_DIR, 'fraud_base.pt'))
    print(f"[DONE] Saved Best Fraud Model to {MODEL_SAVE_DIR}")

if __name__ == '__main__':
    run_tuning()
