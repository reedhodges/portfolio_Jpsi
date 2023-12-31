from constants import PI, NC, M, O3S1OCT, alpha_s

# D1 : unpolarized quark, unpolarized J/psi
def D1(z,kT,mu):
    const = (2*alpha_s(mu)**2*O3S1OCT) / (9*PI*NC*M**3*z)
    num = kT**2*z**2*(z**2-2*z+2) + 2*M**2*(z-1)**2
    den = (z**2*kT**2+M**2*(1-z))**2
    return const * num / den

# D1LL : unpolarized quark, LL polarized J/psi
def D1LL(z,kT,mu):
    const = (2*alpha_s(mu)**2*O3S1OCT) / (9*PI*NC*M**3*z)
    num = kT**2*z**2*(z**2-2*z+2) - 4*M**2*(z-1)**2
    den = (z**2*kT**2+M**2*(1-z))**2
    return const * num / den