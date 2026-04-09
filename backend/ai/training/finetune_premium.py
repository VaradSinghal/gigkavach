"""
GigKavach — Premium Fine-tuning with Optuna
Fine-tunes the pre-trained backbone for supervised premium regression.
"""

import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import optuna

# Import Backbone
from pretrain_backbone import DAEBackbone

# Configuration
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dataset_engine', 'data')

class PremiumRegressor(nn.Module):
    def __init__(self, backbone, latent_dim, hidden_dim, dropout):
        super(PremiumRegressor, self).__init__()
        self.backbone = backbone
        self.head = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1) # Regression output
        )

    def forward(self, x):
        with torch.no_grad():
            latent = self.backbone(x)
        return self.head(latent)

class SupervisedDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.FloatTensor(y).view(-1, 1)
    def __len__(self): return len(self.X)
    def __getitem__(self, idx): return self.X[idx], self.y[idx]

def objective(trial):
    # Hyperparameters to tune
    lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)
    hidden_dim = trial.suggest_categorical("hidden_dim", [32, 64, 128])
    dropout = trial.suggest_float("dropout", 0.1, 0.5)

    # Data
    workers_df = pd.read_csv(os.path.join(DATA_DIR, 'workers.csv'))
    # Use workers data for premium calculation
    # (In a real scenario, we'd have policies data, but we use workers + calculated premiums from gen)
    # Actually, we need to calculate 'target' premium for the training.
    # We will use the 'avg_weekly_income' and 'trust_score' to derive a dynamic premium target.
    
    scaler = joblib.load(os.path.join(MODEL_DIR, 'backbone_scaler.joblib'))
    features = joblib.load(os.path.join(MODEL_DIR, 'backbone_features.joblib'))
    
    # We need to ensure we have the same features used in backbone
    # (Since worker data doesn't have claim fields, we use claims joined with workers as our training set)
    claims_df = pd.read_csv(os.path.join(DATA_DIR, 'claims.csv'))
    df = pd.merge(claims_df, workers_df, on='worker_id', suffixes=('', '_w'))
    
    for col in ['city', 'zone', 'claim_type', 'primary_platform', 'vehicle_type']:
        le = joblib.load(os.path.join(MODEL_DIR, f'le_{col}.joblib'))
        df[col] = le.transform(df[col].astype(str))
    
    X = df[features].values
    X_scaled = scaler.transform(X)
    # Target: simulate a fair premium (e.g. payout / trust_score)
    # Using 'payout_amount' as a proxy for risk level
    y = df['payout_amount'] / (df['trust_score'] + 0.1)
    y = y.values

    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    train_loader = DataLoader(SupervisedDataset(X_train, y_train), batch_size=32, shuffle=True)
    val_loader = DataLoader(SupervisedDataset(X_val, y_val), batch_size=32)

    latent_dim = 64
    backbone_model = DAEBackbone(X_scaled.shape[1], latent_dim)
    backbone_model.encoder.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'backbone_encoder.pth')))
    model = PremiumRegressor(backbone_model.encoder, latent_dim, hidden_dim, dropout)

    optimizer = optim.Adam(model.head.parameters(), lr=lr)
    criterion = nn.HuberLoss()

    model.train()
    for _ in range(10):
        for xb, yb in train_loader:
            optimizer.zero_grad()
            out = model(xb)
            loss = criterion(out, yb)
            loss.backward()
            optimizer.step()

    model.eval()
    total_val_loss = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            out = model(xb)
            total_val_loss += mean_absolute_error(yb.cpu().numpy(), out.cpu().numpy())
    
    return total_val_loss / len(val_loader)

def run_fine_tuning():
    print("-" * 60)
    print("  GigKavach - Premium Fine-tuning (Optuna)")
    print("-" * 60)

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=15)

    print(f"\n[OPTUNA] Best MAE: {study.best_value:.4f}")
    print(f"[OPTUNA] Best Params: {study.best_params}")

    bp = study.best_params
    
    # Reload data
    claims_df = pd.read_csv(os.path.join(DATA_DIR, 'claims.csv'))
    workers_df = pd.read_csv(os.path.join(DATA_DIR, 'workers.csv'))
    df = pd.merge(claims_df, workers_df, on='worker_id', suffixes=('', '_w'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'backbone_scaler.joblib'))
    features = joblib.load(os.path.join(MODEL_DIR, 'backbone_features.joblib'))
    for col in ['city', 'zone', 'claim_type', 'primary_platform', 'vehicle_type']:
        le = joblib.load(os.path.join(MODEL_DIR, f'le_{col}.joblib'))
        df[col] = le.transform(df[col].astype(str))
    X = df[features].values
    X_scaled = scaler.transform(X)
    y = (df['payout_amount'] / (df['trust_score'] + 0.1)).values
    
    train_loader = DataLoader(SupervisedDataset(X_scaled, y), batch_size=32, shuffle=True)

    latent_dim = 64
    backbone_model = DAEBackbone(X_scaled.shape[1], latent_dim)
    backbone_model.encoder.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'backbone_encoder.pth')))
    model = PremiumRegressor(backbone_model.encoder, latent_dim, bp['hidden_dim'], bp['dropout'])

    optimizer = optim.Adam(model.parameters(), lr=bp['lr'])
    criterion = nn.HuberLoss()

    print(f"\n[2/2] Training Final Premium Model...")
    for epoch in range(25):
        model.train()
        total_loss = 0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            out = model(xb)
            loss = criterion(out, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch+1}/25 | Loss: {total_loss/len(train_loader):.6f}")

    torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'premium_model_final.pth'))
    
    model.eval()
    with torch.no_grad():
        out = model(torch.FloatTensor(X_scaled))
        report = {
            "model_type": "Fine-tuned Tabular Backbone (DAE + Regressor)",
            "mae": float(mean_absolute_error(y, out.numpy())),
            "r2": float(r2_score(y, out.numpy())),
            "params": bp
        }
        joblib.dump(report, os.path.join(MODEL_DIR, 'premium_report.joblib'))

    print(f"\n[SUCCESS] Final Premium Model Saved.")
    print("-" * 60)

if __name__ == "__main__":
    run_fine_tuning()
