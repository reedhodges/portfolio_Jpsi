import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

def feature_engineering(data):
    data = data.copy()
    # total cross section
    data['total_U'] = data[['oct3s1_U_grid', 'oct1s0_U_grid', 'oct3p0_U_grid', 'sing3s1_U_grid']].sum(axis=1)
    data['total_L'] = data[['oct3s1_L_grid', 'oct1s0_L_grid', 'oct3p0_L_grid', 'sing3s1_L_grid']].sum(axis=1)
    data['total'] = data['total_U'] + data['total_L']
    # ratios
    data['Q2overX'] = data['Q']**2/data['x']
    data['XoverZ'] = data['x']/data['z']
    # squared parameters
    data['x2'] = data['x']**2
    data['z2'] = data['z']**2
    data['Q2'] = data['Q']**2
    data['PT2'] = data['PT']**2
    return data

def z_score_filter(data, threshold=3):
    z_scores = np.abs(stats.zscore(data.select_dtypes(include=[np.number])))
    filtered_data = data[(z_scores < threshold).all(axis=1)]
    return filtered_data

def scale_data(data):
    data = data.copy()
    scaler = MinMaxScaler()
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
    return data

def preprocess_data(data):
    data = data.copy()
    data.dropna(inplace=True)
    data = z_score_filter(data)
    data = scale_data(data)
    return data

def process_data(filepath):
    try:
        data = pd.read_csv(filepath)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None
    data = feature_engineering(data)
    data = preprocess_data(data)
    return data