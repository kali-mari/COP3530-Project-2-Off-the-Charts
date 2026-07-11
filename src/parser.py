import pandas as pd
import numpy as np

FEATURE_COLS = [
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'time_signature'
]

def load_data(filepath='../data/dataset.csv'):
    df = pd.read_csv(filepath)
    df = df.dropna(subset=FEATURE_COLS)
    return df

def get_feature_matrix(df):
    matrix = df[FEATURE_COLS].values.astype(float)
    mins = matrix.min(axis=0)
    maxs = matrix.max(axis=0)
    normalized = (matrix - mins) / (maxs - mins + 1e-8)
    return normalized