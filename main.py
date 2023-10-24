import numpy as np
import pandas as pd
from cross_sections import differential_cross_section, total_sigma_U, u_interp, d_interp, g_interp
from constants import S, O3S1SING, O1S0OCT, O3P0OCT

# domains for the kinematic variables
x_domain = np.linspace(0.1, 0.99, 10)
z_domain = np.linspace(0.1, 0.8, 10)
Q_domain = np.linspace(10., 50., 10)
PT_domain = np.linspace(0.01, 6., 50)

# functions to compute the percentage of d_sigma contributions from the various LDMEs
def percent_O3S1OCT(x, z, Q, PT):
    d_sigma = differential_cross_section(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)
    return d_sigma.FF.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)

def percent_O1S0OCT(x, z, Q, PT):
    d_sigma = differential_cross_section(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)
    return d_sigma.PGF.oct1s0.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)

def percent_O3P0OCT(x, z, Q, PT):
    d_sigma = differential_cross_section(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)
    return d_sigma.PGF.oct3p0.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)

def percent_O3S1SING(x, z, Q, PT):
    d_sigma = differential_cross_section(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)
    return d_sigma.PGF.sing3s1.U(x, z, Q, PT) / total_sigma_U(x, z, Q, PT)

#print(percent_O3S1OCT(0.1, 0.5, 10., 1.))

# generate grids
x_grid, z_grid, Q_grid, PT_grid = np.meshgrid(x_domain, z_domain, Q_domain, PT_domain)

# compute percentage of d_sigma contributions on the grid
percent_O3S1OCT_grid = percent_O3S1OCT(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
percent_O1S0OCT_grid = percent_O1S0OCT(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
percent_O3P0OCT_grid = percent_O3P0OCT(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
percent_O3S1SING_grid = percent_O3S1SING(x_grid.ravel(), z_grid.ravel(), Q_grid.ravel(), PT_grid.ravel())
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

#print(df.head)
#print(df.describe())

