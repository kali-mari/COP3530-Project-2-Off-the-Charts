import pandas as pd
import numpy as np
import os

FEATURE_COLS = [
    'danceability', 'energy', 'key', 'loudness', 'mode',
    'speechiness', 'acousticness', 'instrumentalness',
    'liveness', 'valence', 'tempo', 'time_signature'
]


def feature_row_to_list(row, feature_cols=FEATURE_COLS):
    return [row[col] for col in feature_cols]


def feature_vector_distance(query_vector, candidate_vector):
   # turn both vectors into numpy arrays so we can do math on them
    query_array = np.asarray(query_vector, dtype=float)
    candidate_array = np.asarray(candidate_vector, dtype=float)

    if query_array.shape != candidate_array.shape:
        raise ValueError('query_vector and candidate_vector must have the same shape')
    if query_array.shape != (len(FEATURE_COLS),):
        raise ValueError(f'feature vectors must have length {len(FEATURE_COLS)}')

    return float(np.linalg.norm(query_array - candidate_array))


def feature_distance(query_vector, candidate_vector):
    # just a thin wrapper so the heap code has a short name to call
    return feature_vector_distance(query_vector, candidate_vector)


def find_query_song(df, title, track_name_col='track_name'):

    if track_name_col not in df.columns:
        raise ValueError(f"'{track_name_col}' column was not found in the dataframe")

    normalized_title = str(title).strip().lower()
    track_names = df[track_name_col].astype(str).str.strip().str.lower()
    matching_df = df.loc[track_names == normalized_title]

    if matching_df.empty:
        raise ValueError(
            f"No song found with title '{title}' in column '{track_name_col}'"
        )

    if len(matching_df) > 1:
        print(f"Multiple songs matched '{title}'. Using the first match:")
        for row_index, row in matching_df.iterrows():
            artists = row['artists'] if 'artists' in matching_df.columns else 'Unknown artist'
            print(f"- index {row_index}: {row[track_name_col]} by {artists}")

    selected_index, selected_row = next(iter(matching_df.iterrows()))
    feature_vector = feature_row_to_list(selected_row)
    return selected_index, feature_vector


def build_index_feature_pairs(df, feature_cols=FEATURE_COLS):
    #turns the whole dataframe into the (index, feature_vector) pairs that
    #find_k_nearest expects as its song_vectors argument.
    
    return [
        (index, feature_row_to_list(row, feature_cols))
        for index, row in df[feature_cols].iterrows()
    ]


DEFAULT_MINMAX_COLS = [
    'danceability', 'energy', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'key', 'time_signature'
]

DEFAULT_ZSCORE_COLS = ['tempo', 'loudness']

def load_data(filepath=None, impute_time_sig=True, genre_col='track_genre'):
    if filepath is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(base_dir, 'data', 'dataset.csv')

    df = pd.read_csv(filepath)
    df = df.dropna(subset=FEATURE_COLS)
    if impute_time_sig:
        df, _ = impute_time_signature_by_genre(df, genre_col=genre_col)
    return df

def get_feature_matrix(df):
    matrix = df[FEATURE_COLS].values.astype(float)
    mins = matrix.min(axis=0)
    maxs = matrix.max(axis=0)
    normalized = (matrix - mins) / (maxs - mins + 1e-8)
    return normalized


def impute_time_signature_by_genre(df, genre_col='track_genre'):
    if 'time_signature' not in df.columns:
        return df, {}
 
    valid = df[df['time_signature'].astype(float) != 0]
    medians = {}
    if not valid.empty and genre_col in valid.columns:
        medians = valid.groupby(genre_col)['time_signature'].median().to_dict()
 
    try:
        global_median = int(valid['time_signature'].median()) if not valid.empty else 4
    except Exception:
        global_median = 4

    mask = df['time_signature'].astype(float) == 0
    if genre_col in df.columns:
        df.loc[mask, 'time_signature'] = (
            df.loc[mask, genre_col].map(medians).fillna(global_median).astype(int)
        )
    else:
        df.loc[mask, 'time_signature'] = global_median

    return df, medians


def apply_minmax_scaling(df, cols):

    mins = df[cols].min()
    maxs = df[cols].max()
    denom = (maxs - mins).replace(0, 1e-8)
    df[cols] = (df[cols] - mins) / denom
    return df, {'mins': mins.to_dict(), 'maxs': maxs.to_dict()}


def apply_zscore_scaling(df, cols):

    means = df[cols].mean()
    stds = df[cols].std()
    stds = stds.replace(0, 1e-8)
    df[cols] = (df[cols] - means) / stds
    return df, {'means': means.to_dict(), 'stds': stds.to_dict()}


def normalize_features(df, minmax_cols=None, zscore_cols=None, impute_time_sig=False, genre_col='track_genre'):
   
    scalers = {'minmax': {}, 'zscore': {}, 'impute': {}}
    if impute_time_sig:
        df, medians = impute_time_signature_by_genre(df, genre_col=genre_col)
        scalers['impute'] = medians

    if minmax_cols is None:
        minmax_cols = DEFAULT_MINMAX_COLS
    if zscore_cols is None:
        zscore_cols = DEFAULT_ZSCORE_COLS

    if minmax_cols:
        df, mm = apply_minmax_scaling(df, minmax_cols)
        scalers['minmax'] = mm

    if zscore_cols:
        df, zs = apply_zscore_scaling(df, zscore_cols)
        scalers['zscore'] = zs

    return df, scalers


def prepare_song_database(filepath=None, impute_time_sig=True, genre_col='track_genre'):
    
    #  convenience one stop function for main.py
    
    df = load_data(filepath=filepath, impute_time_sig=impute_time_sig, genre_col=genre_col)
    df, scalers = normalize_features(df, impute_time_sig=False, genre_col=genre_col)
    song_vectors = build_index_feature_pairs(df)
    return df, song_vectors, scalers
