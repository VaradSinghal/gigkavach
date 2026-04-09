"""
GigKavach — Advanced AI Pre-training
Implements a Self-Supervised Denoising AutoEncoder (DAE) as a backbone for tabular data.
"""

import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dataset_engine', 'data')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'saved_models')
os.makedirs(MODEL_DIR, exist_ok=True)

class DAEBackbone(nn.Module):
    """Denoising AutoEncoder Backbone for Tabular Feature Learning."""
    def __init__(self, input_dim, latent_dim=64):
        super(DAEBackbone, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.1),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, latent_dim),
            nn.ReLU()
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Linear(256, input_dim)
        )

    def forward(self, x):
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return latent, reconstructed

class TabularDataset(Dataset):
    def __init__(self, data):
        self.data = torch.FloatTensor(data)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        return self.data[idx]

def pretrain():
    print("-" * 60)
    print("  GigKavach - Self-Supervised Backbone Pre-training")
    print("-" * 60)

    # 1. Load and Merge Data
    claims_df = pd.read_csv(os.path.join(DATA_DIR, 'claims.csv'))
    workers_df = pd.read_csv(os.path.join(DATA_DIR, 'workers.csv'))
    
    # Merge for a rich feature set
    df = pd.merge(claims_df, workers_df, on='worker_id', suffixes=('', '_w'))
    
    # Select features for pre-training (all relevant continuous + encoded categorical)
    num_cols = [
        'inactive_hours', 'payout_amount', 'rainfall_mm', 'aqi', 'temperature_c',
        'avg_daily_hours', 'experience_weeks', 'avg_daily_income', 'avg_weekly_income',
        'latitude', 'longitude', 'trust_score'
    ]
    cat_cols = ['city', 'zone', 'claim_type', 'primary_platform', 'vehicle_type']
    
    # Fill missing
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    
    # Encode Categorical
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        joblib.dump(le, os.path.join(MODEL_DIR, f'le_{col}.joblib'))
    
    features = num_cols + cat_cols
    X = df[features].values
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'backbone_scaler.joblib'))
    joblib.dump(features, os.path.join(MODEL_DIR, 'backbone_features.joblib'))

    # Build Dataloader
    dataset = TabularDataset(X_scaled)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

    # Initialize Model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DAEBackbone(X_scaled.shape[1]).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 2. Training Loop (Denoising)
    epochs = 50
    print(f"[1/2] Training Backbone with Denoising Task ({epochs} epochs)...")
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in dataloader:
            batch = batch.to(device)
            
            # Add noise (Denoising AutoEncoder)
            noise = torch.randn_like(batch) * 0.1
            noisy_batch = batch + noise
            
            optimizer.zero_grad()
            _, reconstructed = model(noisy_batch)
            loss = criterion(reconstructed, batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/{epochs} | Loss: {total_loss/len(dataloader):.6f}")

    # 3. Save Backbone
    torch.save(model.encoder.state_dict(), os.path.join(MODEL_DIR, 'backbone_encoder.pth'))
    # Save full model for potential reuse
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, 'backbone_full.pth'))
    
    print(f"\n[SUCCESS] Backbone Saved to: {MODEL_DIR}")
    print("-" * 60)

if __name__ == "__main__":
    pretrain()
