from math import sin
from scipy import integrate
import numpy as np

# Function with four separate arguments
def f(x, y, z):
    return sin(x * y * z)

ans, _ = integrate.tplquad(f, 1, 2, 2, 3, 0, 1)

print(ans)