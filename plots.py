import pandas as pd
import matplotlib.pyplot as plt

from data_processing import process_data

filepath = 'cs_data/cross_sections.csv'
processed_data = process_data(filepath)

desired_cols = ['x', 'z', 'Q', 'PT', 'oct3s1_U_grid']
df = processed_data[desired_cols]

# pick a random value of x, z, and Q from the columns
x = df['x'].sample().values[0]
z = df['z'].sample().values[0]
Q = df['Q'].sample().values[0]

# create a dataframe with only the rows that have the chosen values of x, z, and Q
df = df[(df['x'] == x) & (df['z'] == z) & (df['Q'] == Q)]

# plot the cross section as a function of PT
plt.plot(df['PT'], df['oct3s1_U_grid'], 'o')
plt.xlabel('PT (GeV)')
plt.ylabel('d sigma / d PT^2 (pb/GeV^2)')
plt.title(f'Color octet 3s1 diff. cross section \n x = {round(x,2)}, z = {round(z,2)}, Q = {round(Q,2)} GeV')
plt.show()


