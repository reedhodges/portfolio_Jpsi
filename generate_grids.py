import numpy as np
import pandas as pd
import os

from cross_sections import differential_cross_section
from constants import S, O3S1OCT, O3S1SING, O1S0OCT, O3P0OCT

d_sigma = differential_cross_section(S, O3S1OCT, O3S1SING, O1S0OCT, O3P0OCT)
    
domains = {
    'x_domain': np.linspace(0.1, 0.99, 25),
    'z_domain': np.linspace(0.1, 0.8, 25),
    'Q_domain': np.linspace(10., 50., 25),
    'PT_domain': np.linspace(0.01, 6., 75)
}

x_grid, z_grid, Q_grid, PT_grid = np.meshgrid(
    domains['x_domain'], domains['z_domain'], domains['Q_domain'], domains['PT_domain']
)

# compute d_sigma contributions on the grid
def compute_grid_values(d_sigma, x_grid, z_grid, Q_grid, PT_grid):
    grid_values = {}
    for process in ['FF', 'PGF']:
        for pol in ['U', 'L']:
            if process == 'FF':
                key = f'oct3s1_{pol}_grid'
                func = getattr(d_sigma.FF, pol)
                grid_values[key] = func(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
            elif process == 'PGF':
                for ldme in ['oct1s0', 'oct3p0', 'sing3s1']:
                    key = f'{ldme}_{pol}_grid'
                    nested_class_instance = getattr(d_sigma.PGF, ldme)
                    func = getattr(nested_class_instance, pol)
                    grid_values[key] = func(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
    return grid_values

grid_values = compute_grid_values(d_sigma, x_grid, z_grid, Q_grid, PT_grid)

data = {
    'x': x_grid.ravel(),
    'z': z_grid.ravel(),
    'Q': Q_grid.ravel(),
    'PT': PT_grid.ravel()
}

for key, value in grid_values.items():
    data[key] = value

df = pd.DataFrame(data)

# the proper domain for PT is actually a function of z and Q, 
# so need to remove the ones that violate the domain.
# first need to define the bins in z and Q
def z_bin(z):
    return np.piecewise(z, [z < 0.4, z >= 0.4], [0.1, 0.4])
def Q_bin(Q):
    return np.piecewise(Q, [Q < 30., Q >= 30.], [10., 30.])
# apply these piecewise functions to the dataframe values
z_bin_min = df['z'].apply(lambda x: z_bin(x))
Q_bin_min = df['Q'].apply(lambda x: Q_bin(x))
# define a condition on PT
condition = df['PT'] <= z_bin_min * Q_bin_min / 2.
# remove the rows that violate the condition
df = df.loc[condition]

print(df.describe())

# save dataframe to csv
cwd = os.getcwd()
subdir = 'cs_data'
filename = 'cross_sections.csv'
savepath = os.path.join(cwd, subdir, filename)
df.to_csv(savepath, index=False)