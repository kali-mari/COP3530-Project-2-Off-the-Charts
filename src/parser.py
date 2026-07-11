import pandas as pd
import numpy as np
import os

FEATURE_COLS = [
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'time_signature'
]

def load_data():
    # builds the path relative to this file's location, not wherever you run from
    base_dir = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(base_dir, 'data', 'dataset.csv')
    
    df = pd.read_csv(filepath)
    df = df.dropna(subset=FEATURE_COLS)
    return df

def get_feature_matrix(df):
    matrix = df[FEATURE_COLS].values.astype(float)
    mins = matrix.min(axis=0)
    maxs = matrix.max(axis=0)
    normalized = (matrix - mins) / (maxs - mins + 1e-8)
    return normalized