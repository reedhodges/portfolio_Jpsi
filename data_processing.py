import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from scipy import stats

orig_dependent_vars = ['oct3s1_U_grid', 'oct3s1_L_grid', 'oct1s0_U_grid', 'oct1s0_L_grid', 'oct3p0_U_grid', 'oct3p0_L_grid', 'sing3s1_U_grid', 'sing3s1_L_grid']

def destroy_data(data, col, percent_to_destroy=0.01):
    '''
    Destroys a percentage of the data in a column by replacing it with NaNs.
    '''
    data = data.copy()
    rows_to_destroy = np.random.choice(data.index, size=int(len(data)*percent_to_destroy))
    data.loc[rows_to_destroy, col] = np.nan    
    return data

def add_noise(data, col):
    '''
    Adds noise to a column by adding or subtracting up to 10% of the value.
    '''
    data = data.copy()
    noise = np.random.uniform(-0.1, 0.1, data[col].shape)
    data[col] = data[col] * (1 + noise)
    return data

def mess_up_data(data, percent_to_destroy=0.01):
    '''
    Adds noise and destroys a percentage of the data in each column in orig_dependent_vars.
    '''
    data = data.copy()
    for col in orig_dependent_vars:
        data = add_noise(data, col)
        data = destroy_data(data, col, percent_to_destroy)
    return data

def feature_engineering(data):
    '''
    Adds new features to the data.
    '''
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

def handle_na(data):
    '''
    Imputes missing values with the mean.
    '''
    data = data.copy()
    imputer = SimpleImputer(strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)
    return data

def z_score_filter(data, threshold=3):
    '''
    Filters out rows with z-scores greater than the threshold.
    '''
    z_scores = np.abs(stats.zscore(data.select_dtypes(include=[np.number])))
    filtered_data = data[(z_scores < threshold).all(axis=1)]
    return filtered_data

def label_dominant_mechanisms(data, threshold_for_dominance=0.3):
    '''
    Adds columns to the data that labels whether that mechanism is the dominant mechanism.
    '''
    data = data.copy()
    new_cols = orig_dependent_vars.copy()
    new_cols = [col[:-4] + '_dom' for col in new_cols]
    for pol in ['U', 'L']:
        for ldme in ['oct3s1', 'oct1s0', 'oct3p0', 'sing3s1']:
            condition = data[ldme + '_' + pol + '_grid'] > threshold_for_dominance * data['total_' + pol]
            data[ldme + '_' + pol + '_dom'] = condition.astype(int)
    return data

def scale_data(data):
    '''
    Scales the data using min-max scaling.
    '''
    data = data.copy()
    scaler = MinMaxScaler()
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
    return data

def preprocess_data(data):
    '''
    Handles missing values, filters out outliers, and scales the data.
    '''
    data = data.copy()
    data = handle_na(data)
    data = label_dominant_mechanisms(data)
    data = z_score_filter(data)
    data = scale_data(data)
    # if column name ends in _dom, then it is a binary column and should be an integer
    for col in data.columns:
        if col.endswith('_dom'):
            data[col] = data[col].astype(int)
    return data

def process_data(filepath):
    '''
    Adds new features, messes up the data, and preprocesses the data.
    '''
    try:
        data = pd.read_csv(filepath)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None
    data = feature_engineering(data)
    data = mess_up_data(data, percent_to_destroy=0.01)
    data = preprocess_data(data)
    return data