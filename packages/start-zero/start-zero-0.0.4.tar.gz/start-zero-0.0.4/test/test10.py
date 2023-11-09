import numpy as np

from sz.core.layers import Linear
from sz.functions.all_fun import sigmoid, mean_squared_error

np.random.seed(0)
x = np.random.rand(100, 1)
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)
l1 = Linear(10)
l2 = Linear(1)

def predict(x):
    y = l1(x)
    y = sigmoid(y)
    y = l2(y)
    return y

lr = 0.2
iters = 10000

for i in range(iters):
    y_pred = predict(x)
    loss = mean_squared_error(y, y_pred)

    l1.clear_tensors()
    l2.clear_tensors()
    loss.backward()

    for l in [l1, l2]:
        for p in l.params():
            p.data -= lr * p.grad.data
    if i%1000 == 0:
        print(loss)
