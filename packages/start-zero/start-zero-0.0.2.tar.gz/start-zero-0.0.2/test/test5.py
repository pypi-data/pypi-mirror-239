import numpy as np

from sz.core.tensor import Tensor

x = Tensor(np.array(2.0))
y = x ** 2
y.backward()
gx = x.grad
x.clear_tensor()

z = gx ** 3 + y
z.backward()
print(x.grad)  # 100.0
"""
Tensor(100.0)
"""