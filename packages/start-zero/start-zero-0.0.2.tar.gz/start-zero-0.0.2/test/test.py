import numpy as np

from sz.core.tensor import Tensor

t1 = Tensor(np.array([2]))
t2 = Tensor(np.array(1))
t_12 = t1 + t2
print(t_12.data)

t3 = 18
t4 = Tensor(np.array(1))
t_34 = t3 + t4
print(t_34.data)

t5 = np.array(3)
t6 = Tensor(np.array([1]))
t_56 = t5 + t6
print(t_56.data)

t_1234 = t1 + t2 - t3 + t4
print(t_1234.data)

t7 = Tensor(22)
t8 = Tensor(np.array([10]))
t_78 = t7 + t8
print(t_78.data)

t9 = np.array(12)
t_79 = t7 + t9
print(t_79.data)

t10 = Tensor(np.array([2, 1, 4]))
t11 = Tensor(np.array([3, 5, 2]))
t_1011 = t10 + t11
print(t_1011.data)

t12 = Tensor(np.array([2, 1, 4]))
t_12 = t12 ** 3
print(t_12.data)
"""
[3]
19
[4]
[-14]
[32]
34
[5 6 6]
[ 8  1 64]
"""
