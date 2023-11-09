import math

import numpy as np

from sz.core.tensor import Tensor
from sz.functions.all_fun import power, neg, sub, mul, add

print(power(math.e, 3).data)

x0 = Tensor(np.array(1.0))
x1 = Tensor(np.array(2.0))

y1 = x0 + 11
y2 = 12 + x1
print(y1.data)
print(y2.data)
y3 = x0 - 11
y4 = 12 - x1
print(y3.data)
print(y4.data)
y5 = x0 * 11
y6 = 12 * x1
print(y5.data)
print(y6.data)
y7 = 11 / x0
y8 = 11 / x1
print(y7.data)
print(y8.data)

y9 = neg(power(sub(mul(add(x0, 10), 3), x1), 2))
print(y9.data)

y10 = -(((x0 + 10) * 3 - x1) ** 2)
print(y10.data)
"""
20.085536923187664
12.0
14.0
-10.0
10.0
11.0
24.0
11.0
5.5
-961.0
-961.0
"""
