import numpy as np

pi = np.pi                      # you know what this is
Nc = 3.                         # number of colors
nf = 5.                         # number of flavors
M = 3.1                         # GeV, mass of J/psi
O3s1oct = 0.3e-2                # GeV^3, 3s1 color octet matrix element
O3s1sing = 1.16                 # GeV^3, 3s1 color singlet matrix element
O1s0oct = 8.9e-2                # GeV^3, 1s0 color octet matrix element
O3p0oct = (M/2.)**2*0.56e-2     # GeV^3, 3p0 color octet matrix element
Lambda = 0.2                    # GeV, QCD scale parameter
alpha_em = 1/137.036            # fine structure constant
s = 63.**2                      # GeV^2, center of mass energy squared
to_pb = 1/(2.568e-9)            # conversion factor from GeV^-2 to pb

# strong coupling
def alpha_s(mu):
    return (2*pi)/((11-2/3*nf)*np.log(mu/Lambda))