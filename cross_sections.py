from constants import PI, M, ALPHA_EM, alpha_s, O3S1SING, O1S0OCT, O3P0OCT, S, TO_PB
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
    return np.exp(-PT**2/avP) / (PI*avP)

# Gaussian 1-z distribution
def gaussian_z(z):
    avz = 0.04
    return np.exp(-(1-z)**2/avz) / np.sqrt(PI*avz)

# cross sections differnetial in x, z, Q, PT
class differential_cross_section:
    def __init__(self, S: float, O3S1SING: float, O1S0OCT: float, O3P0OCT: float, u_interp, d_interp, g_interp):
        self.S: float = S
        self.O3S1SING: float = O3S1SING
        self.O1S0OCT: float = O1S0OCT
        self.O3P0OCT: float = O3P0OCT
        self.u_interp = u_interp
        self.d_interp = d_interp
        self.g_interp = g_interp
        self.ff = self.FF(self)
        self.pgf = self.PGF(self)

    # cross sections for light quark fragmentation
    class FF:
        def __init__(self, parent):
            self.parent = parent
        
        # unpolarized J/psi
        def U(x, z, Q, PT):
            y = Q**2/(x*S)
            const = TO_PB*((4*PI*ALPHA_EM**2)/(Q**4)) * (1-y+y**2/2)
            pdf = (2./3.)**2*u_interp((x,Q)) + (1./3.)**2*d_interp((x,Q))
            return const*pdf*3*D1(z,PT,M)
        
        # longitudinally polarized J/psi
        def L(x, z, Q, PT):
            y = Q**2/(x*S)
            const = TO_PB*((4*PI*ALPHA_EM**2)/(Q**4)) * (1-y+y**2/2)
            pdf = (2./3.)**2*u_interp((x,Q)) + (1./3.)**2*d_interp((x,Q))
            return const*pdf*(D1(z,PT,M)-D1LL(z,PT,M))

    # cross sections for photon-gluon fusino    
    class PGF:
        def __init__(self, parent):
            self.parent = parent
            self.Oct1s0 = self.oct1s0(self)
            self.Oct3p0 = self.oct3p0(self)
            self.Sing3s1 = self.sing3s1(self)

        # 1s0 color octet channel
        class oct1s0:
            def __init__(self, parent):
                self.parent = parent

            # unpolarized J/psi
            def U(x, z, Q, PT):
                y = Q**2/(x*S)
                zt = 2-z
                const = TO_PB*(1-y+y**2/2)*32*PI**3*z*ALPHA_EM**2*alpha_s(30)/(9*M*Q**6*zt**3)
                pdf = g_interp((x*zt,Q))
                return const*pdf*gaussian_z(z)*gaussian_PT(PT)*O1S0OCT
            
            # longitudinally polarized J/psi
            def L(x, z, Q, PT):
                y = Q**2/(x*S)
                zt = 2-z
                const = TO_PB*(1-y+y**2/2)*32*PI**3*z*ALPHA_EM**2*alpha_s(30)/(9*M*Q**6*zt**3)
                pdf = g_interp((x*zt,Q))
                return const*pdf*gaussian_z(z)*gaussian_PT(PT)*O1S0OCT / 3.
            
        # 3p0 color octet channel
        class oct3p0:
            def __init__(self, parent):
                self.parent = parent
            
            # unpolarized J/psi
            def U(x, z, Q, PT):
                y = Q**2/(x*S)
                zt = 2-z
                ypoly = y**2*(8+z*(3*z-8)) + 8*(1-y)*zt - 2*(1-y)*z*zt**2
                const = TO_PB*64*PI**3*z*ALPHA_EM**2*alpha_s(30)/(9*M**3*Q**6*zt**5)
                pdf = g_interp((x*zt,Q))
                return const*ypoly*pdf*gaussian_z(z)*gaussian_PT(PT)*O3P0OCT
            
            # longitudinally polarized J/psi
            def L(x, z, Q, PT):
                y = Q**2/(x*S)
                zt = 2-z
                ypoly = (2-y)**2-2*z*(1-y)
                const = TO_PB*64*PI**3*z**3*ALPHA_EM**2*alpha_s(30)/(9*M**3*Q**6*zt**5)
                pdf = g_interp((x*zt,Q))
                return const*ypoly*pdf*gaussian_z(z)*gaussian_PT(PT)*O3P0OCT
        
        # 3s1 color singlet channel
        class sing3s1:
            def __init__(self, parent):
                self.parent = parent
            
            # unpolarized J/psi
            def U(x, z, Q, PT):
                y = Q**2/(x*S)
                zt = 2-z
                zb = 1-z
                const = TO_PB*512*PI*zb*ALPHA_EM**2*alpha_s(30)**2/(243*M*Q**6*z*zt**2)
                PTpoly = (PT**2 + zb**2*M**2*(2-z*zt)) / ((PT**2 + zb**2*M**2)**2)
                pdf = g_interp((x,Q))
                return const*(1-y+y**2/2.)*pdf*PTpoly*O3S1SING
            
            # longitudinally polarized J/psi
            def L(x, z, Q, PT):
                y = Q**2/(x*S)
                zt = 2-z
                zb = 1-z
                const = TO_PB*512*PI*zb*ALPHA_EM**2*alpha_s(30)**2/(243*M*Q**6*z*zt**2)
                PTpoly = PT**2 / ((PT**2 + zb**2*M**2)**2)
                pdf = g_interp((x,Q))
                return const*(1-y+y**2/2.)*pdf*PTpoly*O3S1SING

d_sigma = differential_cross_section(S, O3S1SING, O1S0OCT, O3P0OCT, u_interp, d_interp, g_interp)

print(d_sigma.FF.U(0.1, 0.5, 10., 1.))
print(d_sigma.FF.L(0.1, 0.5, 10., 1.))
print(d_sigma.PGF.oct1s0.U(0.1, 0.5, 10., 1.))
print(d_sigma.PGF.oct1s0.L(0.1, 0.5, 10., 1.))
print(d_sigma.PGF.oct3p0.U(0.1, 0.5, 10., 1.))
print(d_sigma.PGF.oct3p0.L(0.1, 0.5, 10., 1.))
print(d_sigma.PGF.sing3s1.U(0.1, 0.5, 10., 1.))
print(d_sigma.PGF.sing3s1.L(0.1, 0.5, 10., 1.))