import pandas as pd
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt

# read PDF csv files from the data folder
df_u = pd.read_csv('pdf_data/uPDF.csv')
df_d = pd.read_csv('pdf_data/dPDF.csv')
df_g = pd.read_csv('pdf_data/gPDF.csv')

# name the columns of these dataframes
column_names = ['x', 'Q', 'f']
df_u.columns = column_names
df_d.columns = column_names
df_g.columns = column_names

#print(df_u.shape)
#print(df_u.head)

def create_interpolator(df):
    # Extract and sort the unique x and Q values, because RegularGridInterpolator needs them to be in increasing order
    x_values = sorted(df['x'].unique())
    Q_values = sorted(df['Q'].unique())
    
    # Create a matrix of function values using reindexed dataframe
    # this reindexes the dataframe so that its index is a multi-level index of the x and Q values
    # then it unstacks the dataframe, which creates a matrix of function values
    f_values = df.set_index(['x', 'Q']).reindex(index=pd.MultiIndex.from_product([x_values, Q_values])).unstack().values
    
    # Create an interpolating function
    return RegularGridInterpolator((x_values, Q_values), f_values, method='linear')

# Compute interpolators
u_interp = create_interpolator(df_u)
d_interp = create_interpolator(df_d)
g_interp = create_interpolator(df_g)

# x domain for plot
x_range = np.linspace(0.01, 0.99, 100)
Q_value = 10.

y1 = x_range * u_interp((x_range, Q_value))
y2 = x_range * d_interp((x_range, Q_value))
y3 = (x_range * g_interp((x_range, Q_value)))/10.

plt.semilogx(x_range, y1, label='u')
plt.semilogx(x_range, y2, label='d')
plt.semilogx(x_range, y3, label='g/10')
plt.legend()
plt.show()