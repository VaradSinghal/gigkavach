import torch
import torch.nn as nn
import torch.optim as optim
import os

class GigKavachNet(nn.Module):
    """
    Modular Multi-Layer Perceptron (MLP) for GigKavach.
    Supports both Regression (Premium Pricing) and Classification (Fraud).
    """
    def __init__(self, input_dim, hidden_layers=[64, 32], output_dim=1, dropout=0.2, task='regression'):
        super(GigKavachNet, self).__init__()
        
        layers = []
        last_dim = input_dim
        
        for h_dim in hidden_layers:
            layers.append(nn.Linear(last_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            last_dim = h_dim
        
        layers.append(nn.Linear(last_dim, output_dim))
        
        if task == 'classification':
            layers.append(nn.Sigmoid())
            
        self.network = nn.Sequential(*layers)
        self.task = task

    def forward(self, x):
        return self.network(x)

    def save(self, path):
        """Save the model weights and architecture state."""
        torch.save({
            'state_dict': self.state_dict(),
            'config': {
                'input_dim': self.input_dim_cache, # Need to cache these during init or train
                'hidden_layers': self.hidden_layers_cache,
                'output_dim': self.output_dim_cache,
                'dropout': self.dropout_cache,
                'task': self.task
            }
        }, path)

def create_model(input_dim, hidden_layers, output_dim, dropout, task):
    """Factory to create and track config."""
    model = GigKavachNet(input_dim, hidden_layers, output_dim, dropout, task)
    model.input_dim_cache = input_dim
    model.hidden_layers_cache = hidden_layers
    model.output_dim_cache = output_dim
    model.dropout_cache = dropout
    return model

def load_model(path, map_location='cpu'):
    """Load model from file."""
    checkpoint = torch.load(path, map_location=map_location)
    config = checkpoint['config']
    model = create_model(
        config['input_dim'], 
        config['hidden_layers'], 
        config['output_dim'], 
        config['dropout'], 
        config['task']
    )
    model.load_state_dict(checkpoint['state_dict'])
    return model
