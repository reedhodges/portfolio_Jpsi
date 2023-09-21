import scipy.tplquad as tplquad

def bin_integrate(sigma,bin,PT)
    return tplquad(lambda x, z, Q: sigma(x,z,Q,PT), bin[2,0], bin[2,1], bin[1,0], bin[1,1], bin[0,0], bin[0,1])