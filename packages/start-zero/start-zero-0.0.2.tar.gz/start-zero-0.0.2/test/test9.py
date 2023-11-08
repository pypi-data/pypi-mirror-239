import numpy as np

from sz.core.tensor import Tensor, Parameter

x = Tensor(np.array(1.0))
y = Parameter(np.array(2.0))
z = x * y
print(isinstance(x, Parameter))
print(isinstance(y, Parameter))
print(isinstance(z, Parameter))
print(z, z.data)
