import numpy as np

from sz.core import cuda
from sz.core.config import Config
from sz.core.tensor import Tensor
from sz.core.utils import reshape_sum_backward, log_sum_exp, max_backward_shape, as_array
from sz.functions.base_fun import Function


def setup_tensor():
    Tensor.__add__ = add
    Tensor.__radd__ = add
    Tensor.__sub__ = sub
    Tensor.__rsub__ = rsub
    Tensor.__mul__ = mul
    Tensor.__rmul__ = rmul
    Tensor.__truediv__ = div
    Tensor.__rtruediv__ = rdiv
    Tensor.__pow__ = power
    Tensor.__neg__ = neg
    Tensor.__mod__ = mod
    Tensor.__rmod__ = rmod
    Tensor.dot = matmul
    Tensor.max = max
    Tensor.min = min


# ====================================================================================================
# 所有的函数方法（all functions）
# ====================================================================================================

# ---------- 基本函数（加[+]、减[-]、乘[*]、除[/]、幂[**]、负数[-]、模[%]） start ----------
def add(x0, x1):
    return Add()(x0, x1)


def sub(x0, x1):
    return Sub()(x0, x1)


def rsub(x0, x1):
    return Sub()(x1, x0)


def mul(x0, x1):
    return Mul()(x0, x1)


def rmul(x0, x1):
    return Mul()(x0, x1)


def div(x0, x1):
    return Div()(x0, x1)


def rdiv(x0, x1):
    return Div()(x1, x0)


def power(x, c):
    return Power(c)(x)


def neg(x):
    return Neg()(x)


def mod(x0, x1):
    return Mod()(x0, x1)


def rmod(x0, x1):
    return Mod()(x1, x0)


# ---------- 基本函数（加[+]、减[-]、乘[*]、除[/]、幂[**]、负数[-]、模[%]） end ----------

# ---------- 三角函数（正弦[sin]、余弦[cos]、正切[tan]、双曲正切[tanh]） start ----------
def sin(x):
    return Sin()(x)


def cos(x):
    return Cos()(x)


def tan(x):
    return Tan()(x)


def tanh(x):
    return Tanh()(x)


# ---------- 三角函数（正弦[sin]、余弦[cos]、正切[tan]、双曲正切[tanh]） end ----------

# ---------- 指数对数函数（e为底的指数[exp]、10为底的对数[lg]、e为底的对数[ln]） start ----------
def exp(x):
    return Exp()(x)


def lg(x):
    return Lg()(x)


def ln(x):
    return Ln()(x)


# ---------- 指数对数函数（e为底的指数[exp]、10为底的对数[lg]、e为底的对数[ln]） end ----------

# ---------- 辅助函数（合并求和[sum_to]、广播[broadcast_to]、求和[sum]、平均数[average]、矩阵相乘[matmul]、矩阵转置[transpose]、重塑形状[reshape]、线性回归[linear]） start ----------
def sum_to(x, shape):
    if x.shape == shape:
        return x
    return SumTo(shape)(x)


def broadcast_to(x, shape):
    if x.shape == shape:
        return x
    return BroadcastTo(shape)(x)


def sum(x, axis=None, keepdims=False):
    return Sum(axis, keepdims)(x)


def average(x, axis=None, keepdims=False):
    y = sum(x, axis, keepdims)
    return y * (y.data.size / (x.data.size if isinstance(x, Tensor) else x.size))


def matmul(x0, x1):
    return MatMul()(x0, x1)


def transpose(x, axes=None):
    return Transpose(axes)(x)


def reshape(x, shape):
    return Reshape(shape)(x)


def linear(x, W, b=None):
    return Linear()(x, W, b)


# ---------- 辅助函数（合并求和[sum_to]、广播[broadcast_to]、求和[sum]、平均数[average]、矩阵相乘[matmul]、矩阵转置[transpose]、重塑形状[reshape]、线性回归[linear]） end ----------

# ---------- 激活函数（S型生长曲线[sigmoid]、线性整流函数[ReLU]、归一化指数函数[softmax]、归一化指数函数[log_softmax]、线性整流函数[leaky_relu]） start ----------
def sigmoid(x):
    return Sigmoid()(x)


def relu(x):
    return ReLU()(x)


def softmax(x, axis=1):
    """
    简单实现：
    x = as_variable(x)
    y = exp(x)
    sum_y = sum(y, axis=axis, keepdims=True)
    return y / sum_y
    """
    return Softmax(axis)(x)


def log_softmax(x, axis=1):
    return LogSoftmax(axis)(x)


def leaky_relu(x, slope=0.2):
    return LeakyReLU(slope)(x)


# ---------- 激活函数（S型生长曲线[sigmoid]、线性整流函数[ReLU]、归一化指数函数[softmax]、归一化指数函数[log_softmax]、线性整流函数[leaky_relu]） end ----------

# ---------- 损失函数（均方误差[mean_squared_error]、交叉熵损失[softmax_cross_entropy]、交叉熵损失[sigmoid_cross_entropy]、二元交叉熵[binary_cross_entropy]） start ----------
def mean_squared_error(x0, x1):
    """
    简单实现：
    x0, x1 = Tensor(x0), Tensor(x1)
    diff = x0 - x1
    y = sum(diff ** 2) / len(diff)
    return y
    """
    return MeanSquaredError()(x0, x1)


def softmax_cross_entropy(x, t):
    """
    简单实现
    x, t = Tensor(x), Tensor(t)
    N = x.shape[0]
    p = softmax(x)
    p = clip(p, 1e-15, 1.0)  # 避免log(0)
    log_p = log(p)
    tlog_p = log_p[np.arange(N), t.data]
    y = -1 * sum(tlog_p) / N
    return y
    """
    return SoftmaxCrossEntropy()(x, t)


def sigmoid_cross_entropy(x, t):
    if x.ndim != t.ndim:
        t = t.reshape(*x.shape)
    x, t = (x if isinstance(x, Tensor) else Tensor(x)), (t if isinstance(t, Tensor) else Tensor(t))
    N = len(x)
    p = sigmoid(x)
    p = clip(p, 1e-15, 1.0)
    tlog_p = t * ln(p) + (1 - t) * ln(1 - p)
    y = -1 * sum(tlog_p) / N
    return y


def binary_cross_entropy(p, t):
    if p.ndim != t.ndim:
        t = t.reshape(*p.shape)
    N = len(t)
    p = clip(p, 1e-15, 0.999)
    tlog_p = t * ln(p) + (1 - t) * ln(1 - p)
    y = -1 * sum(tlog_p) / N
    return y


# ---------- 损失函数（均方误差[mean_squared_error]、交叉熵损失[softmax_cross_entropy]、交叉熵损失[sigmoid_cross_entropy]、二元交叉熵[binary_cross_entropy]） end ----------

# ---------- 其它函数（最大值[max]、最小值[min]、限定数组上下界[clip]、准确度[accuracy]、退出[dropout]、批量[batch_norm]、嵌入ID[embed_id]） start ----------
def max(x, axis=None, keepdims=False):
    return Max(axis, keepdims)(x)


def min(x, axis=None, keepdims=False):
    return Min(axis, keepdims)(x)


def clip(x, x_min, x_max):
    return Clip(x_min, x_max)(x)


def accuracy(y, t):
    """
    不可微
    """
    y, t = (y if isinstance(y, Tensor) else Tensor(y)), (t if isinstance(t, Tensor) else Tensor(t))
    pred = y.data.argmax(axis=1).reshape(t.shape)
    result = (pred == t.data)
    acc = result.average()
    return Tensor(as_array(acc))


def dropout(x, dropout_ratio=0.5):
    if not isinstance(x, Tensor):
        x = Tensor(x)
    if Config.TRAIN:
        xp = cuda.get_array_module(x)
        mask = xp.random.rand(*x.shape) > dropout_ratio
        scale = xp.array(1.0 - dropout_ratio).astype(x.dtype)
        y = x * mask / scale
        return y
    else:
        return x


def batch_norm(x, gamma, beta, mean, var, decay=0.9, eps=2e-5):
    return BatchNorm(mean, var, decay, eps)(x, gamma, beta)


def embed_id(x, W):
    return W[x]


# ---------- 其它函数（最大值[max]、最小值[min]、限定数组上下界[clip]、准确度[accuracy]、退出[dropout]、批量[batch_norm]、嵌入ID[embed_id]） end ----------

# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- 分割线（具体实现） --------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ====================================================================================================
# 基本函数（加[+]、减[-]、乘[*]、除[/]、幂[**]、负数[-]、模[%]）
# ====================================================================================================
class Add(Function):
    """
    加法类
    """

    def __init__(self):
        """
        初始化
        """
        self.x0_shape = None
        self.x1_shape = None

    def forward(self, x0, x1):
        """
        加法的正向传播
        :param x0: 加法的一个值
        :param x1: 加法的另一个值
        :return: 一个值与另一个值相加的结果
        """
        return x0 + x1

    def backward(self, gy):
        """
        加法的反向传播
        :param gy: 导数值
        :return: 加法反向传播的值
        """
        gx0, gx1 = gy, gy
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if self.x0_shape != self.x1_shape:
            gx0 = sum_to(gx0, self.x0_shape)
            gx1 = sum_to(gx1, self.x1_shape)
        return gx0, gx1


class Sub(Function):
    """
    减法类
    """

    def __init__(self):
        self.x0_shape = None
        self.x1_shape = None

    def forward(self, x0, x1):
        """
        减法的正向传播
        :param x0: 被减数
        :param x1: 减数
        :return: 差值
        """
        return x0 - x1

    def backward(self, gy):
        """
        减法的反向传播
        :param gy: 导数值
        :return: 减法反向传播的值
        """
        gx0, gx1 = gy, -gy
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if self.x0_shape != self.x1_shape:
            gx0 = sum_to(gx0, self.x0_shape)
            gx1 = sum_to(gx1, self.x1_shape)
        return gx0, gx1


class Mul(Function):
    """
    乘法类
    """

    def forward(self, x0, x1):
        """
        乘法的正向传播
        :param x0: 一个乘数
        :param x1: 另一个乘数
        :return: 乘积值
        """
        return x0 * x1

    def backward(self, gy):
        """
        乘法的反向传播
        :param gy: 导数值
        :return: 乘法反向传播的值
        """
        x0, x1 = self.inputs
        gx0, gx1 = gy * x1, gy * x0
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if x0.shape != x1.shape:
            gx0 = sum_to(gx0, x0.shape)
            gx1 = sum_to(gx1, x1.shape)
        return gx0, gx1


class Div(Function):
    """
    除法类
    """

    def forward(self, x0, x1):
        """
        除法的正向传播
        :param x0: 被除数
        :param x1: 除数
        :return: 相除的结果
        """
        return x0 / x1

    def backward(self, gy):
        """
        除法的反向传播
        :param gy: 导数值
        :return: 除法反向传播的值
        """
        x0, x1 = self.inputs
        gx0, gx1 = gy / x1, gy * (-x0 / x1 ** 2)
        # 为了处理如数组(2,3)反向传播更新梯度为(1,3)之类的情况
        if x0.shape != x1.shape:
            gx0 = sum_to(gx0, x0.shape)
            gx1 = sum_to(gx1, x1.shape)
        return gx0, gx1


class Power(Function):
    """
    幂类
    """

    def __init__(self, c):
        """
        初始化
        :param c: 常数
        """
        self.c = c

    def forward(self, x):
        """
        幂的正向传播
        :param x: 底数
        :return: 幂值
        """
        return x ** self.c

    def backward(self, gy):
        """
        幂的反向传播
        :param gy: 导数值
        :return: 幂反向传播的值
        """
        x = self.inputs[0]
        c = self.c
        gx = c * (x ** (c - 1)) * gy
        return gx


class Neg(Function):
    """
    负数类
    """

    def forward(self, x):
        """
        负数的正向传播
        :param x: 需要变负的数
        :return: 负值
        """
        return -x

    def backward(self, gy):
        """
        负数的反向传播
        :param gy: 导数值
        :return: 负数反向传播的值
        """
        return -gy


class Mod(Function):
    """
    模类
    """

    def forward(self, x0, x1):
        """
        减法的正向传播
        :param x0: 被取模数
        :param x1: 模数
        :return: 模值
        """
        return x0 % x1

    def backward(self, gy):
        """
        模的反向传播
        简单参考：
        x = 17
        c = 12
        while x > c:
            x = x - c
        print(x, x%c)  # 5 5
        :param gy: 导数值
        :return: 模反向传播的值
        """
        return gy, 0


# ====================================================================================================
# 三角函数（正弦[sin]、余弦[cos]、正切[tan]、双曲正切[tanh]）
# ====================================================================================================
class Sin(Function):
    """
    正弦类
    """

    def forward(self, x):
        """
        正弦的正向传播
        :param x: 待求正弦的值
        """
        xp = cuda.get_array_module(x)
        return xp.sin(x)

    def backward(self, gy):
        """
        正弦的反向传播
        :param gy: 导数值
        :return: 正弦反向传播的值
        """
        x = self.inputs[0]
        return gy * cos(x)


class Cos(Function):
    """
    余弦类
    """

    def forward(self, x):
        """
        余弦的正向传播
        :param x: 待求余弦的值
        """
        xp = cuda.get_array_module(x)
        return xp.cos(x)

    def backward(self, gy):
        """
        余弦的反向传播
        :param gy: 导数值
        :return: 余弦反向传播的值
        """
        x = self.inputs[0]
        return gy * (-sin(x))


class Tan(Function):
    """
    正切类
    """

    def forward(self, x):
        """
        正切的正向传播
        :param x: 待求正切的值
        """
        xp = cuda.get_array_module(x)
        return xp.tan(x)

    def backward(self, gy):
        """
        正切的反向传播
        :param gy: 导数值
        :return: 正切反向传播的值
        """
        x = self.inputs[0]
        return gy * (1 / (cos(x) ** 2))


class Tanh(Function):
    """
    双曲正切类
    """

    def forward(self, x):
        """
        双曲正切的正向传播
        :param x: 待求双曲正切的值
        """
        xp = cuda.get_array_module(x)
        return xp.tanh(x)

    def backward(self, gy):
        """
        双曲正切的反向传播
        :param gy: 导数值
        :return: 双曲正切反向传播的值
        """
        y = self.outputs[0]()  # 弱引用
        # 参见：tanh(x)的导数=1-(tanh(x))^2
        gx = gy * (1 - y * y)
        return gx


# ====================================================================================================
# 指数对数函数（e为底的指数[exp]、10为底的对数[lg]、e为底的对数[ln]）
# ====================================================================================================
class Exp(Function):
    """
    e为底的指数类
    """

    def forward(self, x):
        """
        e为底的指数的正向传播
        :param x: 待求e为底的指数的值
        """
        xp = cuda.get_array_module(x)
        return xp.exp(x)

    def backward(self, gy):
        """
        e为底的指数的反向传播
        :param gy: 导数值
        :return: e为底的指数反向传播的值
        """
        y = self.outputs[0]()  # 弱引用
        gx = gy * y
        return gx


class Lg(Function):
    """
    10为底的对数类
    """

    def forward(self, x):
        """
        10为底的对数的正向传播
        :param x: 待求10为底的对数的值
        """
        xp = cuda.get_array_module(x)
        y = xp.log10(x)
        return y

    def backward(self, gy):
        """
        10为底的对数的反向传播
        :param gy: 导数值
        :return: 10为底的对数反向传播的值
        """
        x = self.inputs[0]
        gx = gy / x
        return gx


class Ln(Function):
    """
    e为底的对数类
    """

    def forward(self, x):
        """
        e为底的对数的正向传播
        :param x: 待求e为底的对数的值
        """
        xp = cuda.get_array_module(x)
        y = xp.log(x)
        return y

    def backward(self, gy):
        """
        e为底的对数的反向传播
        :param gy: 导数值
        :return: e为底的对数反向传播的值
        """
        x = self.inputs[0]
        gx = gy / x
        return gx


# ====================================================================================================
# 辅助函数（合并求和[sum_to]、广播[broadcast_to]、求和[sum]、平均数[average]、矩阵相乘[matmul]、矩阵转置[transpose]、重塑形状[reshape]、线性回归[linear]）
# ====================================================================================================
class SumTo(Function):
    """
    合并求和
    """

    def __init__(self, shape):
        """
        初始化
        :param shape: 合并求和后的数组形状
        """
        self.shape = shape  # 合并求和后的数组形状
        self.x_shape = None  # 待合并求和的数组形状

    def forward(self, x):
        """
        合并求和的正向传播
        :param x: 待合并求和的值
        """
        self.x_shape = x.shape  # 待合并求和的数组形状
        ndim = len(self.shape)  # 合并求和后的数组长度
        lead = x.ndim - ndim  # 待合并求和的数组长度与合并求和后的数组长度差，如(1, 5, 3, 4)->(1, 1)，则差为2
        lead_axis = tuple(range(lead))  # 创造差值的元祖，如差为2，则差值元祖为：(0, 1)
        """
        这是一个用于定位下标的编程技巧，参考：
        temp = ["a", "b", "c", "d"]
        out = tuple([index for index, value in enumerate(temp) if (value == 'a' or value == 'd')])
        print(out)  # (0, 3)
        为什么要筛出sx==1？因为只有求和归一的维度才需要合并，参考：
        x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        print(x.sum((0, 1), keepdims=True))  # (1, 1)
        print(x.sum((0, ), keepdims=True))  # (1, 3)
        print(x.sum((1, ), keepdims=True))  # (4, 1)
        # print(x.sum((0, 1, 2), keepdims=True))  # 报错
        # print(x.sum((2, 2), keepdims=True))  # 报错
        对(1, 1)来说，两个值都是1，因此下标0和1都要被选中；对(1, 3)来说，只有下标为0的才会被选中
        """
        axis = tuple([i + lead for i, sx in enumerate(self.shape) if sx == 1])
        """
        (1, 5, 3, 4)->(1, 1)会先扩充为(0, 1, 1, 1)
        参考元祖相加：
        (1, 2) + (3, 4) = (1, 2, 3, 4)
        """
        y = x.sum(lead_axis + axis, keepdims=True)
        if lead > 0:
            y = y.squeeze(lead_axis)  # 移除扩充的维度
        return y

    def backward(self, gy):
        """
        合并求和的反向传播
        :param gy: 导数值
        :return: 合并求和反向传播的值
        """
        gx = broadcast_to(gy, self.x_shape)
        return gx


class BroadcastTo(Function):
    """
    矩阵广播
    """

    def __init__(self, shape):
        """
        初始化
        :param shape: 广播后的数组形状
        """
        self.shape = shape
        self.x_shape = None

    def forward(self, x):
        """
        广播的正向传播
        :param x: 待合并求和的值
        """
        self.x_shape = x.shape
        xp = cuda.get_array_module(x)
        """
        参考：
        import numpy as np
        from numpy import broadcast_to
        x = np.array([[1, 2]])
        y = broadcast_to(x, (4, 2))
        print(y)
        # [[1 2]
        #  [1 2]
        #  [1 2]
        #  [1 2]]
        """
        y = xp.broadcast_to(x, self.shape)
        return y

    def backward(self, gy):
        """
        广播的反向传播
        :param gy: 导数值
        :return: 广播的反向传播的值
        """
        gx = sum_to(gy, self.x_shape)
        return gx


class Sum(Function):
    """
    求和
    """

    def __init__(self, axis, keepdims):
        """
        初始化
        :param axis: 要求和的数组的形状
        :param keepdims: 是否保留维度（True：保留维度；False：不保留维度）
        """
        self.axis = axis
        self.keepdims = keepdims
        self.x_shape = None

    def forward(self, x):
        """
        求和的正向传播
        :param x: 待求和的值
        """
        self.x_shape = x.shape
        return x.sum(axis=self.axis, keepdims=self.keepdims)

    def backward(self, gy):
        """
        求和的反向传播
        :param gy: 导数值
        :return: 求和的反向传播的值
        """
        gy = reshape_sum_backward(gy, self.x_shape, self.axis, self.keepdims)
        gx = broadcast_to(gy, self.x_shape)
        return gx


class MatMul(Function):
    """
    矩阵相乘
    """

    def forward(self, x0, x1):
        """
        矩阵相乘的正向传播
        :param x0: 一个乘数
        :param x1: 另一个乘数
        """
        return x0.dot(x1)

    def backward(self, gy):
        """
        矩阵相乘的反向传播
        :param gy: 导数值
        :return: 矩阵相乘的反向传播的值
        """
        x0, x1 = self.inputs
        # (3,4)dot(4,2)=(3,2)，对(3,4)的值求导就是(3,2)dot(4,2)的转置矩阵
        gx0 = matmul(gy, x1.T)
        # (3,4)dot(4,2)=(3,2)，对(4,2)的值求导就是(3,4)的转置矩阵dot(3,2)
        gx1 = matmul(x0.T, gy)
        return gx0, gx1


class Transpose(Function):
    """
    矩阵转置
    """

    def __init__(self, axes=None):
        """
        初始化
        :param axes: 轴
        """
        self.axes = axes

    def forward(self, x):
        """
        矩阵转置的正向传播
        :param x: 所要转置的矩阵
        """
        return x.transpose(self.axes)

    def backward(self, gy):
        """
        矩阵转置的反向传播
        :param gy: 导数值
        :return: 矩阵转置的反向传播的值
        """
        if self.axes is None:
            return transpose(gy)
        axes_len = len(self.axes)
        inv_axes = tuple(np.argsort([ax % axes_len for ax in self.axes]))
        return transpose(gy, inv_axes)


class Reshape(Function):
    """
    重塑形状
    """

    def __init__(self, shape):
        """
        初始化
        :param shape: 所要重塑的形状
        """
        self.shape = shape
        self.x_shape = None

    def forward(self, x):
        """
        重塑形状的正向传播
        :param x: 所要转置的矩阵
        """
        self.x_shape = x.shape
        y = x.reshape(self.shape)
        return y

    def backward(self, gy):
        """
        重塑形状的反向传播
        :param gy: 导数值
        :return: 重塑形状的反向传播的值
        """
        return reshape(gy, self.x_shape)


class Linear(Function):
    """
    线性回归：w*x+b
    """

    def forward(self, x, W, b):
        """
        线性回归的正向传播
        :param x: 参数x
        :param W: 参数W
        :param b: 参数b
        :return: 线性回归的计算结果
        """
        y = x.dot(W)
        if b is not None:
            y += b
        return y

    def backward(self, gy):
        """
        线性回归的反向传播
        :param gy: 导数值
        :return: 线性回归的反向传播的值
        """
        x, W, b = self.inputs
        gb = None if b.data is None else sum_to(gy, b.shape)
        gx = matmul(gy, W.T)
        gW = matmul(x.T, gy)
        return gx, gW, gb


# ====================================================================================================
# 激活函数（S型生长曲线[sigmoid]、线性整流函数[ReLU]、归一化指数函数[softmax]、归一化指数函数[log_softmax]、线性整流函数[leaky_relu]）
# ====================================================================================================
class Sigmoid(Function):
    """
    sigmoid
    """

    def forward(self, x):
        """
        sigmoid的正向传播
        :param x: 参数x
        :return: sigmoid函数的计算结果
        """
        xp = cuda.get_array_module(x)
        # y = 1 / (1 + xp.exp(-x))
        y = xp.tanh(x * 0.5) * 0.5 + 0.5  # 更好的实现方式
        return y

    def backward(self, gy):
        """
        sigmoid的反向传播
        :param gy: 导数值
        :return: sigmoid函数的的反向传播的值
        """
        y = self.outputs[0]()
        # 为什么sigmoid(y1)的导数反而是(1-y2)*y2？因为sigmoid(y1)的导数等于sigmoid(y1)*(1-sigmoid(y1))，而y2=sigmoid(y1)，所以替换后就是(1-y2)*y2
        gx = gy * y * (1 - y)
        return gx


class ReLU(Function):
    """
    ReLU
    """

    def forward(self, x):
        """
        ReLU的正向传播
        :param x: 参数x
        :return: ReLU函数的计算结果
        """
        xp = cuda.get_array_module(x)
        y = xp.maximum(x, 0.0)
        return y

    def backward(self, gy):
        """
        ReLU的反向传播
        :param gy: 导数值
        :return: ReLU函数的的反向传播的值
        """
        x, = self.inputs
        mask = x.data > 0
        # mask：True=1、False=0
        gx = gy * mask
        return gx


class Softmax(Function):
    """
    softmax
    """

    def __init__(self, axis=1):
        """
        初始化
        :param axis: 参数axis
        """
        self.axis = axis

    def forward(self, x):
        """
        softmax的正向传播
        :param x: 参数x
        :return: Softmax函数的计算结果
        """
        xp = cuda.get_array_module(x)
        y = x - x.max(axis=self.axis, keepdims=True)
        y = xp.exp(y)
        y /= y.sum(axis=self.axis, keepdims=True)
        return y

    def backward(self, gy):
        """
        softmax的反向传播
        :param gy: 导数值
        :return: softmax函数的的反向传播的值
        """
        y = self.outputs[0]()
        gx = y * gy
        sum_dx = gx.sum(axis=self.axis, keepdims=True)
        gx -= y * sum_dx
        return gx


class LogSoftmax(Function):
    """
    log_softmax
    """

    def __init__(self, axis=1):
        """
        初始化
        :param axis: 参数axis
        """
        self.axis = axis

    def forward(self, x):
        """
        log_softmax的正向传播
        :param x: 参数x
        :return: log_softmax函数的计算结果
        """
        xp = cuda.get_array_module(x)
        log_z = log_sum_exp(xp, x, self.axis)
        y = x - log_z
        return y

    def backward(self, gy):
        """
        log_softmax的反向传播
        :param gy: 导数值
        :return: log_softmax函数的的反向传播的值
        """
        y = self.outputs[0]()
        gx = gy - exp(y) * gy.sum(axis=self.axis, keepdims=True)
        return gx


class LeakyReLU(Function):
    """
    leaky_relu
    """

    def __init__(self, slope):
        """
        初始化
        :param slope: 参数slope
        """
        self.slope = slope

    def forward(self, x):
        """
        leaky_relu的正向传播
        :param x: 参数x
        :return: leaky_relu函数的计算结果
        """
        y = x.copy()
        y[x <= 0] *= self.slope
        return y

    def backward(self, gy):
        """
        leaky_relu的反向传播
        :param gy: 导数值
        :return: leaky_relu函数的的反向传播的值
        """
        x, = self.inputs
        mask = (x.data > 0).astype(gy.dtype)
        mask[mask <= 0] = self.slope
        gx = gy * mask
        return gx


# ====================================================================================================
# 损失函数（均方误差[mean_squared_error]、交叉熵损失[softmax_cross_entropy]、交叉熵损失[sigmoid_cross_entropy]、二元交叉熵[binary_cross_entropy]）
# ====================================================================================================
class MeanSquaredError(Function):
    """
    mean_squared_error
    """

    def forward(self, x0, x1):
        """
        mean_squared_error的正向传播
        :param x0: 参数x0
        :param x1: 参数x1
        :return: mean_squared_error函数的计算结果
        """
        diff = x0 - x1
        y = (diff ** 2).sum() / len(diff)
        return y

    def backward(self, gy):
        """
        mean_squared_error的反向传播
        :param gy: 导数值
        :return: mean_squared_error函数的的反向传播的值
        """
        x0, x1 = self.inputs
        diff = x0 - x1
        gx0 = gy * diff * (2. / len(diff))
        gx1 = -gx0
        return gx0, gx1


class SoftmaxCrossEntropy(Function):
    """
    softmax_cross_entropy
    """

    def forward(self, x, t):
        """
        softmax_cross_entropy的正向传播
        :param x: 参数x
        :param t: 参数t
        :return: softmax_cross_entropy函数的计算结果
        """
        xp = cuda.get_array_module(x)
        N = x.shape[0]
        log_z = log_sum_exp(xp, x, axis=1)
        log_p = x - log_z
        log_p = log_p[np.arange(N), t.ravel()]
        y = -log_p.sum() / np.float32(N)
        return y

    def backward(self, gy):
        """
        softmax_cross_entropy的反向传播
        :param gy: 导数值
        :return: softmax_cross_entropy函数的的反向传播的值
        """
        x, t = self.inputs
        N, CLS_NUM = x.shape
        gy *= 1 / N
        y = softmax(x)
        xp = cuda.get_array_module(t.data)
        t_onehot = xp.eye(CLS_NUM, dtype=t.dtype)[t.data]
        y = (y - t_onehot) * gy
        return y


# =============================================================================
# 其它函数（最大值[max]、最小值[min]、限定数组上下界[clip]、准确度[accuracy]、退出[dropout]、批量[batch_norm]、嵌入ID[embed_id]）
# =============================================================================
class Max(Function):
    """
    max
    """

    def __init__(self, axis=None, keepdims=False):
        """
        初始化
        :param axis: 参数axis
        :param keepdims: 参数keepdims
        """
        self.axis = axis
        self.keepdims = keepdims

    def forward(self, x):
        """
        max的正向传播
        :param x: 参数x
        :return: max函数的计算结果
        """
        y = x.max(axis=self.axis, keepdims=self.keepdims)
        return y

    def backward(self, gy):
        """
        max的反向传播
        :param gy: 导数值
        :return: max函数的的反向传播的值
        """
        x = self.inputs[0]
        y = self.outputs[0]()  # 弱引用
        shape = max_backward_shape(x, self.axis)
        gy = reshape(gy, shape)
        y = reshape(y, shape)
        cond = (x.data == y.data)
        gy = broadcast_to(gy, cond.shape)
        return gy * cond


class Min(Max):
    """
    min
    """

    def forward(self, x):
        """
        min的正向传播
        :param x: 参数x
        :return: min函数的计算结果
        """
        y = x.min(axis=self.axis, keepdims=self.keepdims)
        return y


class Clip(Function):
    """
    clip
    """

    def __init__(self, x_min, x_max):
        """
        初始化
        :param x_min: 最小值
        :param x_max: 最大值
        """
        self.x_min = x_min
        self.x_max = x_max

    def forward(self, x):
        """
        clip的正向传播
        :param x: 参数x
        :return: clip函数的计算结果
        """
        xp = cuda.get_array_module(x)
        y = xp.clip(x, self.x_min, self.x_max)
        return y

    def backward(self, gy):
        """
        clip的反向传播
        :param gy: 导数值
        :return: clip函数的的反向传播的值
        """
        x, = self.inputs
        mask = (x.data >= self.x_min) * (x.data <= self.x_max)
        gx = gy * mask
        return gx


class BatchNorm(Function):
    """
    batch_norm
    """

    def __init__(self, mean, var, decay, eps):
        """
        初始化
        :param mean: 参数mean
        :param var: 参数var
        :param decay: 参数decay
        :param eps: 参数eps
        """
        self.avg_mean = mean
        self.avg_var = var
        self.decay = decay
        self.eps = eps
        self.inv_std = None

    def forward(self, x, gamma, beta):
        """
        batch_norm的正向传播
        :param x: 参数x
        :param gamma: 参数gamma
        :param beta: 参数beta
        :return: batch_norm函数的计算结果
        """
        assert x.ndim == 2 or x.ndim == 4

        x_ndim = x.ndim
        if x_ndim == 4:
            N, C, H, W = x.shape
            # (N, C, H, W) -> (N * H * W, C)
            x = x.transpose(0, 2, 3, 1).reshape(-1, C)

        xp = cuda.get_array_module(x)

        if Config.TRAIN:
            mean = x.mean(axis=0)
            var = x.var(axis=0)
            inv_std = 1 / xp.sqrt(var + self.eps)
            xc = (x - mean) * inv_std

            m = x.size // gamma.size
            s = m - 1. if m - 1. > 1. else 1.
            adjust = m / s  # unbiased estimation
            self.avg_mean *= self.decay
            self.avg_mean += (1 - self.decay) * mean
            self.avg_var *= self.decay
            self.avg_var += (1 - self.decay) * adjust * var
            self.inv_std = inv_std
        else:
            inv_std = 1 / xp.sqrt(self.avg_var + self.eps)
            xc = (x - self.avg_mean) * inv_std
        y = gamma * xc + beta

        if x_ndim == 4:
            # (N * H * W, C) -> (N, C, H, W)
            y = y.reshape(N, H, W, C).transpose(0, 3, 1, 2)
        return y

    def backward(self, gy):
        """
        batch_norm的反向传播
        :param gy: 导数值
        :return: batch_norm函数的的反向传播的值
        """
        gy_ndim = gy.ndim
        if gy_ndim == 4:
            N, C, H, W = gy.shape
            gy = gy.transpose(0, 2, 3, 1).reshape(-1, C)

        x, gamma, beta = self.inputs
        batch_size = len(gy)

        if x.ndim == 4:
            N, C, H, W = x.shape
            x = x.transpose(0, 2, 3, 1).reshape(-1, C)
        mean = x.sum(axis=0) / batch_size
        xc = (x - mean) * self.inv_std

        gbeta = sum(gy, axis=0)
        ggamma = sum(xc * gy, axis=0)
        gx = gy - gbeta / batch_size - xc * ggamma / batch_size
        gx *= gamma * self.inv_std

        if gy_ndim == 4:
            gx = gx.reshape(N, H, W, C).transpose(0, 3, 1, 2)
        return gx, ggamma, gbeta
