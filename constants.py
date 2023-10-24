import numpy as np

PI = np.pi     
# number of colors                 
NC = 3.   
# number of flavors                      
NF = 5.     
# GeV, mass of J/psi                    
M = 3.1         
# GeV^3, 3s1 color octet matrix element               
O3S1OCT = 0.3e-2       
# GeV^3, 3s1 color singlet matrix element         
O3S1SING = 1.16   
# GeV^3, 1s0 color octet matrix element              
O1S0OCT = 8.9e-2     
# GeV^3, 3p0 color octet matrix element           
O3P0OCT = (M/2.)**2*0.56e-2     
# GeV, QCD scale parameter
LAMBDA = 0.2            
# fine structure constant        
ALPHA_EM = 1/137.036    
# GeV^2, center of mass energy squared        
S = 63.**2      
# conversion factor from GeV^-2 to pb
TO_PB = 1/(2.568e-9)
            
# strong coupling
def alpha_s(mu):
    return (2*PI)/((11-2/3*NF)*np.log(mu/LAMBDA))