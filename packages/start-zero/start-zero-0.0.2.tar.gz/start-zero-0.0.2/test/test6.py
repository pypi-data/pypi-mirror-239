import numpy as np

from sz.core.tensor import Tensor
from sz.functions.all_fun import sum_to, sum

# import cupy as cp


x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
y = sum(x, axis=0)
y.backward()
print(y)
print(x.grad)

x = Tensor(np.random.randn(2, 3, 4, 5))
y = sum(x, keepdims=True)
print(y.shape)

x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
y = sum_to(x, (1, 3))
print(y)

y = sum_to(x, (2, 1))
print(y)

x0 = Tensor(np.array([1, 2, 3]))
x1 = Tensor(np.array([10]))
y = x0 + x1
print(y)
y.backward()
print(x1.grad)

# print(cp.asnumpy(np.array([1, 2, 3])))
"""
Tensor([5 7 9])
Tensor([[1 1 1]
          [1 1 1]])
(1, 1, 1, 1)
Tensor([[5 7 9]])
Tensor([[ 6]
          [15]])
Tensor([11 12 13])
Tensor([1 1 1])
"""