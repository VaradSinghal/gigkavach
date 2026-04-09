"""
GigKavach — Fraud Fine-tuning with Optuna
Fine-tunes the pre-trained backbone for supervised fraud classification.
"""

import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score
import joblib
import optuna

# Import Backbone
from pretrain_backbone import DAEBackbone

# Configuration
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dataset_engine', 'data')

class FraudClassifier(nn.Module):
    def __init__(self, backbone, latent_dim, hidden_dim, dropout):
        super(FraudClassifier, self).__init__()
        self.backbone = backbone # encoder only
        self.head = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        with torch.no_grad(): # Keep backbone frozen or fine-tune slowly
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
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])

    # Data
    claims_df = pd.read_csv(os.path.join(DATA_DIR, 'claims.csv'))
    workers_df = pd.read_csv(os.path.join(DATA_DIR, 'workers.csv'))
    df = pd.merge(claims_df, workers_df, on='worker_id', suffixes=('', '_w'))
    
    scaler = joblib.load(os.path.join(MODEL_DIR, 'backbone_scaler.joblib'))
    features = joblib.load(os.path.join(MODEL_DIR, 'backbone_features.joblib'))
    
    # Pre-process
    cat_cols = ['city', 'zone', 'claim_type', 'primary_platform', 'vehicle_type']
    for col in cat_cols:
        le = joblib.load(os.path.join(MODEL_DIR, f'le_{col}.joblib'))
        df[col] = le.transform(df[col].astype(str))
    
    X = df[features].values
    X_scaled = scaler.transform(X)
    y = df['is_legitimate'].map({True: 0, False: 1}).values # Fraud is positive class (1)

    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    train_loader = DataLoader(SupervisedDataset(X_train, y_train), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(SupervisedDataset(X_val, y_val), batch_size=batch_size)

    # Initialize Model with Backbone
    latent_dim = 64
    backbone_model = DAEBackbone(X_scaled.shape[1], latent_dim)
    backbone_model.encoder.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'backbone_encoder.pth')))
    model = FraudClassifier(backbone_model.encoder, latent_dim, hidden_dim, dropout)

    optimizer = optim.Adam(model.head.parameters(), lr=lr)
    criterion = nn.BCELoss()

    # Simple Train Loop for Optuna
    model.train()
    for epoch in range(10): # Shorter for tuning
        for xb, yb in train_loader:
            optimizer.zero_grad()
            out = model(xb)
            loss = criterion(out, yb)
            loss.backward()
            optimizer.step()

    # Evaluate
    model.eval()
    all_preds = []
    all_y = []
    with torch.no_grad():
        for xb, yb in val_loader:
            out = model(xb)
            all_preds.extend(out.cpu().numpy())
            all_y.extend(yb.cpu().numpy())
    
    score = roc_auc_score(all_y, all_preds)
    return score

def run_fine_tuning():
    print("-" * 60)
    print("  GigKavach - Fraud Fine-tuning (Optuna)")
    print("-" * 60)

    # 1. Hyperparameter Optimization
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=15)

    print(f"\n[OPTUNA] Best ROC-AUC: {study.best_value:.4f}")
    print(f"[OPTUNA] Best Params: {study.best_params}")

    # 2. Final Training with Best Params
    bp = study.best_params
    
    # Reload data for full training
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
    y = df['is_legitimate'].map({True: 0, False: 1}).values
    
    train_loader = DataLoader(SupervisedDataset(X_scaled, y), batch_size=bp['batch_size'], shuffle=True)

    latent_dim = 64
    backbone_model = DAEBackbone(X_scaled.shape[1], latent_dim)
    backbone_model.encoder.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'backbone_encoder.pth')))
    model = FraudClassifier(backbone_model.encoder, latent_dim, bp['hidden_dim'], bp['dropout'])

    optimizer = optim.Adam(model.parameters(), lr=bp['lr']) # Fine-tune entire model now
    criterion = nn.BCELoss()

    print(f"\n[2/2] Training Final Fraud Model...")
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

    # 3. Save Final Model
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'fraud_model_final.pth'))
    
    # Generate Report Stats (Simplified)
    model.eval()
    with torch.no_grad():
        out = model(torch.FloatTensor(X_scaled))
        preds = (out.numpy() > 0.5).astype(int)
        
        report = {
            "model_type": "Fine-tuned Tabular Backbone (DAE + MLP)",
            "roc_auc": float(roc_auc_score(y, out.numpy())),
            "f1": float(f1_score(y, preds)),
            "precision": float(precision_score(y, preds)),
            "recall": float(recall_score(y, preds)),
            "params": bp
        }
        joblib.dump(report, os.path.join(MODEL_DIR, 'fraud_report.joblib'))

    print(f"\n[SUCCESS] Final Fraud Model Saved.")
    print("-" * 60)

if __name__ == "__main__":
    run_fine_tuning()
