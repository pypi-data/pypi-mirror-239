import numpy as np

from sz.core.queue import PriorityQueue
from sz.core.tensor import Tensor
from sz.functions.all_fun import sin

queue = PriorityQueue()
queue.push('a', 8)
queue.push('b', 3)
queue.push('c', 2)
queue.push('d', 1)
queue.push('e', 9)

while queue.len() != 0:
    print(queue.pop())

x = Tensor(np.array(1.0))
y = sin(x)
y.backward()
for i in range(3):
    gx = x.grad
    x.clear_tensor()
    gx.backward()
    print(x.grad.data)
"""
e
a
b
c
d
-0.8414709848078965
-0.5403023058681398
0.8414709848078965
"""