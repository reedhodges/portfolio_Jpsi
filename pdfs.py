import pandas as pd
from scipy.interpolate import RegularGridInterpolator

# read PDF csv files from the data folder
df_u = pd.read_csv('pdf_data/uPDF.csv')
df_d = pd.read_csv('pdf_data/dPDF.csv')
df_g = pd.read_csv('pdf_data/gPDF.csv')

# name the columns of these dataframes
df_u.columns = ['x', 'Q', 'f']
df_d.columns = ['x', 'Q', 'f']
df_g.columns = ['x', 'Q', 'f']

#print(df_u.shape)
#print(df_u.head)

def interpolate_function(df_u):
    # Extract and sort the unique x and Q values, because RegularGridInterpolator needs them to be in increasing order
    x_values = sorted(df_u['x'].unique())
    Q_values = sorted(df_u['Q'].unique())
    
    # Create a matrix of function values using reindexed dataframe
    # this reindexes the dataframe so that its index is a multi-level index of the x and Q values
    # then it unstacks the dataframe, which creates a matrix of function values
    f_values = df_u.set_index(['x', 'Q']).reindex(index=pd.MultiIndex.from_product([x_values, Q_values])).unstack().values
    
    # Create an interpolating function
    interpolator = RegularGridInterpolator((x_values, Q_values), f_values, method='linear')
    
    return interpolator

# Create an interpolating function from the DataFrame
f_interp = interpolate_function(df_u)

x, Q = 0.1, 25
print(f_interp([[x, Q]]))  # Interpolated value at x=1.5, Q=15
