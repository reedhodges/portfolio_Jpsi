import numpy as np

pi = np.pi              # you know what this is
Nc = 3.                 # number of colors
nf = 5.                 # number of flavors
M = 3.1                 # GeV, mass of J/psi
O3s18 = 0.003           # GeV^3, 3s1 color octet matrix element
Lambda = 0.2            # GeV, QCD scale parameter
alpha_em = 1/137.036    # fine structure constant
s = 63.**2              # GeV^2, center of mass energy squared

# strong coupling
def alpha_s(mu):
    return (2*pi)/((11-2/3*nf)*np.log(mu/Lambda))