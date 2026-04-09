"""
GigKavach — Data Pipeline Bridge
Links the backend AI modules to the dataset engine for data generation and loading.
"""

import os
import sys
import pandas as pd

# Find the dataset_engine/scripts path
file_path = os.path.abspath(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))
DATASET_ENGINE_SCRIPTS = os.path.join(ROOT_DIR, 'dataset_engine', 'scripts')

if DATASET_ENGINE_SCRIPTS not in sys.path:
    sys.path.append(DATASET_ENGINE_SCRIPTS)

try:
    from data_gen import generate_all_data as _gen_all
except ImportError:
    print(f"Error: Could not import data_gen from {DATASET_ENGINE_SCRIPTS}")
    def _gen_all(output_dir=None):
        print("Warning: data_gen not found. Using fallback.")
        return None, None, None, None, None

def generate_all_data(output_dir=None):
    """
    Wrapper for the dataset engine's generator.
    Ensures data is generated and returned as DataFrames for training.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Run the generator
    _gen_all(output_dir)
    
    # Load and return the DataFrames as expected by training scripts
    workers_df = pd.read_csv(os.path.join(output_dir, 'workers.csv'))
    weather_df = pd.read_csv(os.path.join(output_dir, 'weather.csv'))
    zones_df = pd.read_csv(os.path.join(output_dir, 'zones.csv'))
    claims_df = pd.read_csv(os.path.join(output_dir, 'claims.csv'))
    
    # earnings.csv might be separate, let's check
    earnings_path = os.path.join(output_dir, 'earnings.csv')
    earnings_df = pd.read_csv(earnings_path) if os.path.exists(earnings_path) else None
    
    return workers_df, weather_df, zones_df, claims_df, earnings_df
