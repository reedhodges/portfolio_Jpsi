from constants import pi, alpha_em, s
from pdfs import f_u, f_d
from fragmentation_functions import D1, D1LL

def d_sigma_L(x, z, Q, PT):
    y = Q**2/(x*s)
    const = ((4*pi*alpha_em**2)/(Q**4)) * (1-y+y**2/2)
    pdf = (2./3.)**2*f_u(x,Q) + (1./3.)**2*f_d(x,Q)
    return const*pdf*(D1(z,PT,Q)-D1LL(z,PT,Q))