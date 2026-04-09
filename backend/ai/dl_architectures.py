"""
GigKavach — Deep Learning Architectures
Shared definitions for the backbone and task-specific heads.
"""

import torch
import torch.nn as nn

class DAEBackbone(nn.Module):
    """Denoising AutoEncoder Backbone for Tabular Feature Learning."""
    def __init__(self, input_dim, latent_dim=64):
        super(DAEBackbone, self).__init__()
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

class FraudClassifier(nn.Module):
    def __init__(self, backbone, latent_dim=64, hidden_dim=128, dropout=0.45):
        super(FraudClassifier, self).__init__()
        self.backbone = backbone
        self.head = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        latent = self.backbone(x)
        return self.head(latent)

class PremiumRegressor(nn.Module):
    def __init__(self, backbone, latent_dim=64, hidden_dim=64, dropout=0.38):
        super(PremiumRegressor, self).__init__()
        self.backbone = backbone
        self.head = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        latent = self.backbone(x)
        return self.head(latent)
