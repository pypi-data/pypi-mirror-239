import numpy as np

from sz.core.tensor import Tensor


def rosenbrock(x0, x1):
    y = 100 * (x1 - x0 ** 2) ** 2 + (x0 - 1) ** 2
    return y


x0 = Tensor(np.array(0.0))
x1 = Tensor(np.array(2.0))
lr = 0.001
iters = 50000

for i in range(iters):
    print(x0, x1)
    x0.clear_tensor()
    x1.clear_tensor()
    y = rosenbrock(x0, x1)
    y.backward()
    x0 -= lr * x0.grad
    x1 -= lr * x1.grad
"""
趋向于：Tensor(0.9999999993721514) Tensor(0.9999999987417905)
"""