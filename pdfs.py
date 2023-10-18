import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt

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

def interpolate_function(df):
    # Extract and sort the unique x and Q values, because RegularGridInterpolator needs them to be in increasing order
    x_values = sorted(df['x'].unique())
    Q_values = sorted(df['Q'].unique())
    
    # Create a matrix of function values using reindexed dataframe
    # this reindexes the dataframe so that its index is a multi-level index of the x and Q values
    # then it unstacks the dataframe, which creates a matrix of function values
    f_values = df.set_index(['x', 'Q']).reindex(index=pd.MultiIndex.from_product([x_values, Q_values])).unstack().values
    
    # Create an interpolating function
    interpolator = RegularGridInterpolator((x_values, Q_values), f_values, method='linear')
    
    return interpolator

# Create interpolating functions from the dataframes
def uPDF(x, Q):
    f_interp = interpolate_function(df_u)
    return f_interp([[x, Q]])[0]

def dPDF(x, Q):
    f_interp = interpolate_function(df_d)
    return f_interp([[x, Q]])[0]

def gPDF(x, Q):
    f_interp = interpolate_function(df_g)
    return f_interp([[x, Q]])[0]

x_range = np.linspace(0.01, 0.99, 100)
y1 = [x*uPDF(x, 10) for x in x_range]
y2 = [x*dPDF(x, 10) for x in x_range]
y3 = [x*gPDF(x, 10)/10.0 for x in x_range]

#plt.semilogx(x_range, y1, label='u')
#plt.semilogx(x_range, y2, label='d')
#plt.semilogx(x_range, y3, label='g/10')
#plt.legend()
#plt.show()

print(uPDF(0.1, 10))