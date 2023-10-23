from constants import pi, M, alpha_em, alpha_s, O3s1sing, O1s0oct, O3p0oct, s, to_pb
from pdfs import df_u, df_d, df_g, create_interpolator
from fragmentation_functions import D1, D1LL
import numpy as np

# Compute interpolators
u_interp = create_interpolator(df_u)
d_interp = create_interpolator(df_d)
g_interp = create_interpolator(df_g)

# Gaussian PT distribution
def gaussian_PT(PT):
    avP = 0.25
    return np.exp(-PT**2/avP) / (pi*avP)

# Gaussian 1-z distribution
def gaussian_z(z):
    avz = 0.04
    return np.exp(-(1-z)**2/avz) / np.sqrt(pi*avz)

# quark fragmentation: unpolarized J/psi
def d_sigma_FF_U(x, z, Q, PT):
    y = Q**2/(x*s)
    const = to_pb*((4*pi*alpha_em**2)/(Q**4)) * (1-y+y**2/2)
    pdf = (2./3.)**2*u_interp((x,Q)) + (1./3.)**2*d_interp((x,Q))
    return const*pdf*3*D1(z,PT,Q)

# quark fragmentation: longitudinal J/psi
def d_sigma_FF_L(x, z, Q, PT):
    y = Q**2/(x*s)
    const = to_pb*((4*pi*alpha_em**2)/(Q**4)) * (1-y+y**2/2)
    pdf = (2./3.)**2*u_interp((x,Q)) + (1./3.)**2*d_interp((x,Q))
    return const*pdf*(D1(z,PT,Q)-D1LL(z,PT,Q))

# photon-gluon fusion: 1s0 octet, unpolarized J/psi
def d_sigma_PGF_1s0oct_U(x, z, Q, PT):
    y = Q**2/(x*s)
    zt = 2-z
    const = to_pb*(1-y+y**2/2)*32*pi**3*z*alpha_em**2*alpha_s(30)/(9*M*Q**6*zt**3)
    pdf = g_interp((x*zt,Q))
    return const*pdf*gaussian_z(z)*gaussian_PT(PT)*O1s0oct

# photon-gluon fusion: 1s0 octet, long. polarized J/psi
def d_sigma_PGF_1s0oct_L(x, z, Q, PT):
    return d_sigma_PGF_1s0oct_U(x, z, Q, PT) / 3.

# photon-gluon fusion: 3p0 octet, unpolarized J/psi
def d_sigma_PGF_3p0oct_U(x, z, Q, PT):
    y = Q**2/(x*s)
    zt = 2-z
    ypoly = y**2*(8+z*(3*z-8)) + 8*(1-y)*zt - 2*(1-y)*z*zt**2
    const = to_pb*64*pi**3*z*alpha_em**2*alpha_s(30)/(9*M**3*Q**6*zt**5)
    pdf = g_interp((x*zt,Q))
    return const*ypoly*pdf*gaussian_z(z)*gaussian_PT(PT)*O3p0oct

# photon-gluon fusion: 3p0 octet, long. polarized J/psi
def d_sigma_PGF_3p0oct_L(x, z, Q, PT):
    y = Q**2/(x*s)
    zt = 2-z
    ypoly = (2-y)**2-2*z*(1-y)
    const = to_pb*64*pi**3*z**3*alpha_em**2*alpha_s(30)/(9*M**3*Q**6*zt**5)
    pdf = g_interp((x*zt,Q))
    return const*ypoly*pdf*gaussian_z(z)*gaussian_PT(PT)*O3p0oct

# photon-gluon fusion: 3s1 singled, unpolarized J/psi
def d_sigma_PGF_3s1sing_U(x, z, Q, PT):
    y = Q**2/(x*s)
    zt = 2-z
    zb = 1-z
    const = to_pb*512*pi*zb*alpha_em**2*alpha_s(30)**2/(243*M*Q**6*z*zt**2)
    PTpoly = (PT**2 + zb**2*M**2*(2-z*zt)) / ((PT**2 + zb**2*M**2)**2)
    pdf = g_interp((x,Q))
    return const*(1-y+y**2/2.)*pdf*PTpoly*O3s1sing

# photon-gluon fusion: 3s1 singled, long. polarized J/psi
def d_sigma_PGF_3s1sing_L(x, z, Q, PT):
    y = Q**2/(x*s)
    zt = 2-z
    zb = 1-z
    const = to_pb*512*pi*zb*alpha_em**2*alpha_s(30)**2/(243*M*Q**6*z*zt**2)
    PTpoly = PT**2 / ((PT**2 + zb**2*M**2)**2)
    pdf = g_interp((x,Q))
    return const*(1-y+y**2/2.)*pdf*PTpoly*O3s1sing

print(d_sigma_FF_U(0.1, 0.5, 10., 1.))
print(d_sigma_FF_L(0.1, 0.5, 10., 1.))
print(d_sigma_PGF_1s0oct_U(0.1, 0.5, 10., 1.))
print(d_sigma_PGF_1s0oct_L(0.1, 0.5, 10., 1.))
print(d_sigma_PGF_3p0oct_U(0.1, 0.5, 10., 1.))
print(d_sigma_PGF_3p0oct_L(0.1, 0.5, 10., 1.))
print(d_sigma_PGF_3s1sing_U(0.1, 0.5, 10., 1.))
print(d_sigma_PGF_3s1sing_L(0.1, 0.5, 10., 1.))