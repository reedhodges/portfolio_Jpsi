import numpy as np
import pandas as pd
from cross_sections import differential_cross_section, total_sigma_U, u_interp, d_interp, g_interp
from constants import S, O3S1SING, O1S0OCT, O3P0OCT
import os

# functions to compute the percentage of d_sigma contributions from the various LDMEs
class percent_contributions:
    def __init__(self, S: float, O3S1SING: float, O1S0OCT: float, O3P0OCT: float, u_interp, d_interp, g_interp):
        self.S: float = S
        self.O3S1SING: float = O3S1SING
        self.O1S0OCT: float = O1S0OCT
        self.O3P0OCT: float = O3P0OCT
        self.u_interp = u_interp
        self.d_interp = d_interp
        self.g_interp = g_interp
        self.d_sigma = differential_cross_section(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)

    # percentage of d_sigma from the 3s1 color octet channel
    def from_O3S1OCT(self, x, z, Q, PT):
        return self.d_sigma.FF.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)
    
    # percentage of d_sigma from the 1s0 color octet channel
    def from_O1S0OCT(self, x, z, Q, PT):
        return self.d_sigma.PGF.oct1s0.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)
    
    # percentage of d_sigma from the 3p0 color octet channel
    def from_O3P0OCT(self, x, z, Q, PT):
        return self.d_sigma.PGF.oct3p0.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)
    
    # percentage of d_sigma from the 3s1 color singlet channel
    def from_O3S1SING(self, x, z, Q, PT):
        return self.d_sigma.PGF.sing3s1.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)
    
# domains for the kinematic variables
x_domain = np.linspace(0.1, 0.99, 10)
z_domain = np.linspace(0.1, 0.8, 10)
Q_domain = np.linspace(10., 50., 10)
PT_domain = np.linspace(0.01, 6., 50)

# generate grids
x_grid, z_grid, Q_grid, PT_grid = np.meshgrid(x_domain, z_domain, Q_domain, PT_domain)

# initialize percentage class instance
percent = percent_contributions(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)

# compute percentage of d_sigma contributions on the grid
percent_O3S1OCT_grid = percent.from_O3S1OCT(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
percent_O1S0OCT_grid = percent.from_O1S0OCT(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
percent_O3P0OCT_grid = percent.from_O3P0OCT(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
percent_O3S1SING_grid = percent.from_O3S1SING(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
total_grid = percent_O3S1OCT_grid + percent_O1S0OCT_grid + percent_O3P0OCT_grid + percent_O3S1SING_grid

# create a pandas dataframe from the grid
df = pd.DataFrame({
    'x': x_grid.ravel(), 
    'z': z_grid.ravel(), 
    'Q': Q_grid.ravel(), 
    'PT': PT_grid.ravel(), 
    'percent_O3S1OCT': percent_O3S1OCT_grid, 
    'percent_O1S0OCT': percent_O1S0OCT_grid,
    'percent_O3P0OCT': percent_O3P0OCT_grid,
    'percent_O3S1SING': percent_O3S1SING_grid,
    'total': total_grid
    })

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
# now define a condition on PT
condition = df['PT'] <= z_bin_min * Q_bin_min / 2.
# now remove the rows that violate the condition
df = df.loc[condition]

# remote outliers from the dataframe with Z-score of more than 3
df['z_score_O3S1OCT'] = np.abs((df['percent_O3S1OCT'] - df['percent_O3S1OCT'].mean())/df['percent_O3S1OCT'].std())
df['z_score_O1S0OCT'] = np.abs((df['percent_O1S0OCT'] - df['percent_O1S0OCT'].mean())/df['percent_O1S0OCT'].std())
df['z_score_O3P0OCT'] = np.abs((df['percent_O3P0OCT'] - df['percent_O3P0OCT'].mean())/df['percent_O3P0OCT'].std())
df['z_score_O3S1SING'] = np.abs((df['percent_O3S1SING'] - df['percent_O3S1SING'].mean())/df['percent_O3S1SING'].std())

df = df.loc[df['z_score_O3S1OCT'] <= 3.]
df = df.loc[df['z_score_O1S0OCT'] <= 3.]
df = df.loc[df['z_score_O3P0OCT'] <= 3.]
df = df.loc[df['z_score_O3S1SING'] <= 3.]

# drop the z-score columns
df = df.drop(columns=['z_score_O3S1OCT', 'z_score_O1S0OCT', 'z_score_O3P0OCT', 'z_score_O3S1SING'])

# remove rows with negative percentages or percentages greater than 1
df = df.loc[(0. <= df['percent_O3S1OCT']) & (df['percent_O3S1OCT'] <= 1.)]
df = df.loc[(0. <= df['percent_O1S0OCT']) & (df['percent_O1S0OCT'] <= 1.)]
df = df.loc[(0. <= df['percent_O3P0OCT']) & (df['percent_O3P0OCT'] <= 1.)]
df = df.loc[(0. <= df['percent_O3S1SING']) & (df['percent_O3S1SING'] <= 1.)]

#print(df.describe())

# save dataframe to csv
cwd = os.getcwd()
subdir = 'cs_data'
filename = 'percent_contributions.csv'
savepath = os.path.join(cwd, subdir, filename)
df.to_csv(savepath, index=False)