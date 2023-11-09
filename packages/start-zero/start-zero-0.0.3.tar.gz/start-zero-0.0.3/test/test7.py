import numpy as np
import matplotlib.pyplot as plt

from sz.core.tensor import Tensor
from sz.functions.all_fun import matmul, linear, sigmoid, mean_squared_error

x = Tensor(np.array([[1, 2, 3], [4, 5, 6]]))
y = Tensor(np.array([[1, 2], [3, 4], [5, 6]]))
print(matmul(x, y))

np.random.seed(0)
x = np.random.rand(100, 1)
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)

I, H, O = 1, 10, 1
W1 = Tensor(0.01 * np.random.randn(I, H))
b1 = Tensor(np.zeros(H))
W2 = Tensor(0.01 * np.random.randn(H, O))
b2 = Tensor(np.zeros(O))


def predict(x):
    y = linear(x, W1, b1)
    y = sigmoid(y)
    y = linear(y, W2, b2)
    return y


lr = 0.2
iters = 10000

for i in range(iters):
    y_pred = predict(x)
    loss = mean_squared_error(y, y_pred)

    W1.clear_tensor()
    b1.clear_tensor()
    W2.clear_tensor()
    b2.clear_tensor()
    loss.backward()

    W1.data -= lr * W1.grad.data
    b1.data -= lr * b1.grad.data
    W2.data -= lr * W2.grad.data
    b2.data -= lr * b2.grad.data
    if i % 1000 == 0:
        print(loss)


# Plot
plt.scatter(x, y, s=10)
plt.xlabel('x')
plt.ylabel('y')
t = np.arange(0, 1, .01)[:, np.newaxis]
y_pred = predict(t)
plt.plot(t, y_pred.data, color='r')
plt.show()
"""
Tensor([[22 28]
          [49 64]])
Tensor(0.8473695850105871)
Tensor(0.2514286285183606)
Tensor(0.2475948546674987)
Tensor(0.23786120447054826)
Tensor(0.21222231333102934)
Tensor(0.16742181117834185)
Tensor(0.09681932619992686)
Tensor(0.07849528290602335)
Tensor(0.07749729552991157)
Tensor(0.0772213239955932)
"""