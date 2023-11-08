import numpy as np

from sz.core.tensor import Tensor
from sz.functions.all_fun import Power, Exp
from sz.functions.numericaldiff import NumericalDiff

data = np.array(2.0)
x = Tensor(data)
f = Power(2)
fnd1 = NumericalDiff.center_numerical_diff(f, x)
print(fnd1)
fnd2 = NumericalDiff.forward_numerical_diff(f, x)
print(fnd2)

def new_f(_x: Tensor):
    A = Power(2)
    B = Exp()
    C = Power(2)
    return C(B(A(_x)))

x = Tensor(np.array(0.5))
y = NumericalDiff.center_numerical_diff(new_f, x)
print(y)
"""
4.000000000004
4.0001000000078335
3.2974426293330694
"""
