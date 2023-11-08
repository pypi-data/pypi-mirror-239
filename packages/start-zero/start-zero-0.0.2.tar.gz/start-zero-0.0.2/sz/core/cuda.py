import numpy as np

from sz.core.config import Config
from sz.core.tensor import Tensor

cupy_can_use = False
try:
    """
    Windows下安装cupy支持GPU运算：   
    1、N卡支持下载：https://developer.nvidia.com/cuda-downloads   
    2、pip install cupy-cuda12x
    """
    import cupy as cp
    cupy_can_use = True
except ModuleNotFoundError:
    pass


def get_array_module(x):
    if isinstance(x, Tensor):
        x = x.data
    if (not Config.ENABLE_GPU) or (not cupy_can_use):
        return np
    xp = cp.get_array_module(x)
    return xp
